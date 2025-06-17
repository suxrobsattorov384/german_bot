import json
import os
import random
from typing import Dict, List, Optional

class TestLoader:
    def __init__(self, tests_dir="tests"):
        self.tests_dir = tests_dir
        self.cache = {}
        print(f"🔍 TestLoader yaratildi. Tests papkasi: {os.path.abspath(tests_dir)}")
    
    def load_test(self, level: str, kapital: int) -> Optional[Dict]:
        """Testni yuklash"""
        cache_key = f"{level}_{kapital}"
        
        if cache_key in self.cache:
            print(f"✅ Cache'dan olindi: {cache_key}")
            return self.cache[cache_key]
        
        try:
            file_path = f"{self.tests_dir}/{level}/kapital_{kapital}.json"
            full_path = os.path.abspath(file_path)
            
            print(f"🔍 Fayl qidirilmoqda: {full_path}")
            
            if not os.path.exists(file_path):
                print(f"❌ Test fayli topilmadi: {full_path}")
                # Mavjud fayllarni ko'rsatish
                try:
                    level_dir = f"{self.tests_dir}/{level}"
                    if os.path.exists(level_dir):
                        files = os.listdir(level_dir)
                        print(f"📁 {level} papkasidagi fayllar: {files}")
                    else:
                        print(f"📁 {level} papkasi mavjud emas")
                        
                    # Tests papkasidagi papkalar
                    if os.path.exists(self.tests_dir):
                        dirs = os.listdir(self.tests_dir)
                        print(f"📁 Tests papkasidagi papkalar: {dirs}")
                    else:
                        print(f"📁 Tests papkasi mavjud emas: {os.path.abspath(self.tests_dir)}")
                        
                except Exception as e:
                    print(f"❌ Papka tekshirishda xatolik: {e}")
                
                return None
            
            print(f"📖 Fayl o'qilmoqda...")
            with open(file_path, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            
            # Cache'ga saqlash
            self.cache[cache_key] = test_data
            print(f"✅ Test muvaffaqiyatli yuklandi: {level} - Kapital {kapital}")
            print(f"📊 Savollar soni: {len(test_data.get('questions', []))}")
            return test_data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON formatida xatolik: {e}")
            return None
        except Exception as e:
            print(f"❌ Test yuklashda xatolik: {e}")
            return None
    
    def get_questions(self, level: str, kapital: int, count: int = 15, 
                     language: str = 'uz', difficulty: str = None) -> List[Dict]:
        """Savollarni olish"""
        print(f"🔍 Savollar so'ralmoqda: {level} - Kapital {kapital}, Til: {language}")
        
        test_data = self.load_test(level, kapital)
        
        if not test_data:
            print(f"❌ Test ma'lumotlari topilmadi")
            return []
        
        questions = test_data.get('questions', [])
        print(f"📊 Jami savollar: {len(questions)}")
        
        if not questions:
            print(f"❌ Savollar ro'yxati bo'sh")
            return []
        
        # Qiyinlik bo'yicha filtrlash
        if difficulty:
            questions = [q for q in questions if q.get('difficulty') == difficulty]
            print(f"📊 {difficulty} qiyinlikdagi savollar: {len(questions)}")
        
        # Tasodifiy tanlash
        if len(questions) > count:
            questions = random.sample(questions, count)
            print(f"📊 Tanlangan savollar: {count}")
        
        # Tilga moslashtirish
        formatted_questions = []
        for i, q in enumerate(questions):
            try:
                formatted_q = self._format_question(q, language)
                formatted_questions.append(formatted_q)
                print(f"✅ Savol {i+1} formatlandi")
            except Exception as e:
                print(f"❌ Savol {i+1} formatlanmadi: {e}")
        
        print(f"✅ {len(formatted_questions)} ta savol tayyor")
        return formatted_questions
    
    # Qolgan metodlar...
    def _format_question(self, question: Dict, language: str) -> Dict:
        """Savolni formatlash"""
        formatted = question.copy()
        
        if isinstance(question.get('question'), dict):
            formatted['question'] = question['question'].get(language, 
                                   question['question'].get('uz', ''))
        
        if isinstance(question.get('options'), dict):
            formatted['options'] = question['options'].get(language, 
                                  question['options'].get('uz', []))
        
        if isinstance(question.get('explanation'), dict):
            formatted['explanation'] = question['explanation'].get(language, 
                                     question['explanation'].get('uz', ''))
        
        return formatted
    
    def validate_answer(self, question: Dict, user_answer: int) -> Dict:
        """Javobni tekshirish"""
        correct_answer = question.get('correct_answer', -1)
        is_correct = int(user_answer) == int(correct_answer)
        
        result = {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'points': question.get('points', 1) if is_correct else 0,
            'explanation': question.get('explanation', ''),
            'difficulty': question.get('difficulty', 'medium')
        }
        
        return result
    
    def get_test_info(self, level: str, kapital: int, language: str = 'uz') -> Dict:
        """Test ma'lumotlari"""
        test_data = self.load_test(level, kapital)
        
        if not test_data:
            return {}
        
        return {
            'title': test_data.get('title', ''),
            'description': test_data.get('description', ''),
            'total_questions': test_data.get('total_questions', 0),
            'time_limit': test_data.get('time_limit', 1800),
            'passing_score': test_data.get('passing_score', 70),
            'level': test_data.get('level', level),
            'kapital': test_data.get('kapital', kapital)
        }

# Global instance
test_loader = TestLoader()
