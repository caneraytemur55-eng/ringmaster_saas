class MuscleMemoryAIEngine:
    def __init__(self, technique_database):
        self.db = technique_database

    def analyze_movement(self, student_id, technique_code, live_joint_coordinates):
        """
        Sporcunun anlık hareket koordinatlarını ideal teknik matrisiyle kıyaslar.
        """
        ideal_angles = self.db.get_angles(technique_code)
        current_angles = self._calculate_angles(live_joint_coordinates)
        
        # Sapma oranını hesapla (Hata payı analizi)
        deviation_score = self._compare_matrices(ideal_angles, current_angles)
        
        # Kas hafızası skorunu belirle (0 - 100 arası)
        accuracy_score = max(0, 100 - (deviation_score * 1.5))
        
        analysis_result = {
            "student_id": student_id,
            "technique": technique_code,
            "accuracy_score": round(accuracy_score, 2),
            "feedback": self._generate_instant_feedback(deviation_score, current_angles, ideal_angles),
            "requires_coach_intervention": accuracy_score < 65
        }
        
        return analysis_result

    def _calculate_angles(self, coordinates):
        # Eklem noktaları arasındaki açı hesaplamaları (Trigonometrik vektör analizi)
        # Örnek: Dirsek açısı, diz büküm oranı vb.
        return {"elbow_angle": coordinates.get("elbow", 0), "knee_angle": coordinates.get("knee", 0)}

    def _compare_matrices(self, ideal, current):
        # İdeal açı ile mevcut açı arasındaki sapmanın mutlak değeri
        diff_elbow = abs(ideal.get("elbow", 90) - current.get("elbow", 90))
        diff_knee = abs(ideal.get("knee", 180) - current.get("knee", 180))
        return (diff_elbow + diff_knee) / 2

    def _generate_instant_feedback(self, deviation, current, ideal):
        if deviation < 10:
            return "Mükemmel form! Kas hafızası kilitleniyor."
        elif current.get("elbow", 0) > ideal.get("elbow", 90):
            return "Dikkat: Dirseğini çok fazla dışarı açtın, içeri topla!"
        else:
            return "Form bozuluyor, guardını düşürme ve merkeze odaklan."



