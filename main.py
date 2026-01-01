import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def grade(payload: dict) -> dict:
    # Format keywords for prompt
    keywords_text = "\n".join([f"  - {kw['istilah']}: {kw['definisi']}" for kw in payload["keywords"]])
    
    prompt = f"""
Anda adalah penilai otomatis untuk ujian frontend engineering. Setiap soal berisi Masalah, Penyebab, dan Solusi.
Mahasiswa harus menjawab "Sahih" (Valid) atau "Tidak Sahih" (Invalid) dengan reasoning yang mengevaluasi:

1. **Validasi Masalah**: Apakah masalah yang disebutkan realistis dan masuk akal dalam konteks frontend?
2. **Evaluasi Penyebab**: Apakah penyebab yang disebutkan secara logika dan teknis sesuai dengan konteks frontend rendering/behavior?
3. **Evaluasi Solusi**: Apakah solusi menyelesaikan akar masalah, bukan sekadar menghilangkan gejala?

**SOAL:**
Masalah: {payload["masalah"]}
Penyebab: {payload["penyebab"]}
Solusi: {payload["solusi"]}

**KEYWORDS & DEFINISI:**
{keywords_text}

**JAWABAN MAHASISWA:**
Verdict: {payload["verdict"]}
Reasoning: {payload["student_answer"]}

**KRITERIA PENILAIAN KEYWORD:**
- Jika mahasiswa menggunakan istilah dari keywords tetapi SALAH dalam pengertian/definisinya → ini adalah KESALAHAN FATAL, kurangi skor signifikan
- Jika mahasiswa menggunakan konsep/istilah LAIN (bukan dari keywords) tetapi secara logis MASUK AKAL dan relevan → berikan APRESIASI dengan skor lebih tinggi
- Jika mahasiswa menggunakan keywords dengan benar → nilai sesuai kualitas analisisnya

**TUGAS ANDA:**
Nilai apakah verdict dan reasoning mahasiswa BENAR berdasarkan evaluasi ketiga aspek di atas PLUS penggunaan keywords.
Berikan skor maksimal 10 poin dengan breakdown per aspek (total maksimal 10 poin, bukan jumlah dari breakdown).

Return ONLY valid JSON in this exact format:
{{
  "score": 0-10,
  "breakdown": {{
    "validasi_masalah": 0-3.33,
    "evaluasi_penyebab": 0-3.33,
    "evaluasi_solusi": 0-3.34
  }},
  "correct_verdict": "Sahih" atau "Tidak Sahih",
  "keyword_usage": "Penjelasan singkat tentang penggunaan keyword/istilah oleh mahasiswa",
  "feedback": "Feedback singkat dalam bahasa Indonesia mengapa jawaban mahasiswa benar/salah, termasuk apresiasi jika menggunakan konsep alternatif yang baik"
}}
"""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)


def grade_all_students() -> list:
    """Grade all students' answers"""
    # Load questions and answers
    with open("questions.json", encoding="utf-8") as f:
        questions_data = json.load(f)
    
    with open("answers.json", encoding="utf-8") as f:
        answers_data = json.load(f)
    
    # Create question lookup dictionary
    questions_dict = {q["question_id"]: q for q in questions_data["questions"]}
    
    results = []
    
    for student in answers_data["question_answer"]:
        student_result = {
            "student_id": student["student_id"],
            "name": student["name"],
            "grades": []
        }
        
        for answer in student["answers"]:
            question = questions_dict[answer["question_id"]]
            
            # Get student answer text (handle both "answer" and "student_answer" keys)
            student_answer_text = answer.get("answer") or answer.get("student_answer", "")
            
            # Combine question data with student answer for grading
            payload = {
                "masalah": question["masalah"],
                "penyebab": question["penyebab"],
                "solusi": question["solusi"],
                "keywords": question.get("keywords", []),
                "verdict": answer["verdict"],
                "student_answer": student_answer_text
            }
            
            print(f"Grading {student['name']} - {answer['question_id']}...")
            grade_result = grade(payload)
            grade_result["question_id"] = answer["question_id"]
            grade_result["masalah"] = question["masalah"]
            grade_result["penyebab"] = question["penyebab"]
            grade_result["solusi"] = question["solusi"]
            grade_result["student_verdict"] = answer["verdict"]
            grade_result["student_reasoning"] = student_answer_text
            student_result["grades"].append(grade_result)
        
        # Calculate total score
        if student_result["grades"]:
            total_score = sum(g["score"] for g in student_result["grades"]) / len(student_result["grades"])
            student_result["total_score"] = round(total_score, 2)
        else:
            student_result["total_score"] = 0
        
        results.append(student_result)
    
    return results


if __name__ == "__main__":
    results = grade_all_students()
    
    # Save to output file
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*50)
    print("HASIL PENILAIAN")
    print("="*50)
    
    for student in results:
        print(f"\n{student['name']} ({student['student_id']})")
        print(f"Total Score: {student['total_score']}")
        print("-" * 40)
        for grade in student["grades"]:
            print(f"  {grade['question_id']}: {grade['score']}/10")
            print(f"  Masalah: {grade['masalah']}")
            print(f"  Penyebab: {grade['penyebab']}")
            print(f"  Solusi: {grade['solusi']}")
            print(f"  Verdict Mahasiswa: {grade['student_verdict']}")
            print(f"  Verdict Benar: {grade.get('correct_verdict', 'N/A')}")
            if "breakdown" in grade:
                print(f"  Breakdown:")
                for aspect, aspect_score in grade["breakdown"].items():
                    print(f"    - {aspect}: {aspect_score}")
            if "keyword_usage" in grade:
                print(f"  Penggunaan Keyword: {grade['keyword_usage']}")
            print(f"  Feedback: {grade['feedback']}")
            print()
