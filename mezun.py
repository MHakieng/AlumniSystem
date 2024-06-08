import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate
import json
import os

class Student:
    def __init__(self, student_id, name, address, phone, email, nationality, birth_date, foreign_language, interests, gpa, internships, department):
        self.student_id = student_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.nationality = nationality
        self.birth_date = birth_date
        self.foreign_language = foreign_language
        self.interests = interests
        self.gpa = gpa
        self.internships = internships
        self.department = department

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'nationality': self.nationality,
            'birth_date': self.birth_date,
            'foreign_language': self.foreign_language,
            'interests': self.interests,
            'gpa': self.gpa,
            'internships': self.internships,
            'department': self.department
        }

class AlumniSystem:
    def __init__(self, file_name='eleman.txt'):
        self.students = {}
        self.file_name = file_name
        self.load_from_file()

    def register_student(self, student_data):
        student = Student(**student_data)
        self.students[student.student_id] = student
        self.save_to_file()

    def update_student_info(self, student_id, updated_data):
        if student_id in self.students:
            for key, value in updated_data.items():
                setattr(self.students[student_id], key, value)
            self.save_to_file()
        else:
            raise ValueError("Student not found")

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save_to_file()
        else:
            raise ValueError("Student not found")

    def search_student(self, student_id):
        return self.students.get(student_id, None)

    def list_department_students(self, department_name):
        return [student for student in self.students.values() if student.department == department_name]

    def list_high_gpa_students(self):
        return [student for student in self.students.values() if student.gpa > 3.5]

    def list_advanced_english_students(self):
        return [student for student in self.students.values() if student.foreign_language.lower() == 'advanced']

    def save_to_file(self):
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump([student.to_dict() for student in self.students.values()], f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r', encoding='utf-8') as f:
                    students_data = json.load(f)
                    for student_data in students_data:
                        student = Student(**student_data)
                        self.students[student.student_id] = student
            except Exception as e:
                print(f"Error loading from file: {e}")

class AlumniSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mezun Bilgi Sistemi")
        self.system = AlumniSystem()
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._widgets()

    def _widgets(self):
        self.create_student_form()
        self.create_search_frame()
        self.create_buttons()
        self.create_output_box()

    def create_student_form(self):
        self.form_frame = tk.LabelFrame(self.main_frame, text="Öğrenci Bilgileri", padx=10, pady=10)
        self.form_frame.grid(row=0, column=0, sticky="nsew")

        labels = ["ID", "Ad Soyad", "Adres", "Telefon", "E-posta", "Uyruğu", "Doğum Tarihi", "Yabancı Dil Seviyesi", "İlgi Alanları (virgülle ayırın)", "Not Ortalaması", "Staj Bilgileri (şirket;durasyon)", "Bölüm"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = tk.Label(self.form_frame, text=label)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = tk.Entry(self.form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            self.entries[label] = entry

    def create_search_frame(self):
        self.search_frame = tk.LabelFrame(self.main_frame, text="Öğrenci Arama", padx=10, pady=10)
        self.search_frame.grid(row=0, column=1, sticky="nsew")

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Ara", command=self.search_student)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.button_frame, text="Öğrenci Kaydet", command=self.register_student)
        self.register_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_button = tk.Button(self.button_frame, text="Öğrenci Güncelle", command=self.update_student)
        self.update_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self.button_frame, text="Öğrenci Sil", command=self.remove_student)
        self.remove_button.grid(row=0, column=2, padx=5, pady=5)

        self.list_department_button = tk.Button(self.button_frame, text="Bölümdeki Öğrencileri Listele", command=self.list_department_students)
        self.list_department_button.grid(row=0, column=3, padx=5, pady=5)

        self.list_high_gpa_button = tk.Button(self.button_frame, text="Yüksek Not Ortalamasına Sahip Öğrenciler", command=self.list_high_gpa_students)
        self.list_high_gpa_button.grid(row=0, column=4, padx=5, pady=5)

        self.list_advanced_english_button = tk.Button(self.button_frame, text="İleri Seviye İngilizce Bilen Öğrenciler", command=self.list_advanced_english_students)
        self.list_advanced_english_button.grid(row=0, column=5, padx=5, pady=5)

    def create_output_box(self):
        self.output_box = tk.Text(self.main_frame, height=10)
        self.output_box.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def get_student_data_from_form(self):
        data = {}
        for label, entry in self.entries.items():
            data[label] = entry.get()
        return data

    def validate_student_data(self, student_data):
        try:
            student_data['student_id'] = int(student_data.pop('ID'))
            student_data['name'] = student_data.pop('Ad Soyad')
            student_data['address'] = student_data.pop('Adres')
            student_data['phone'] = student_data.pop('Telefon')
            student_data['email'] = student_data.pop('E-posta')
            student_data['nationality'] = student_data.pop('Uyruğu')
            student_data['birth_date'] = student_data.pop('Doğum Tarihi')
            student_data['foreign_language'] = student_data.pop('Yabancı Dil Seviyesi')
            student_data['interests'] = student_data.pop('İlgi Alanları (virgülle ayırın)').split(',')
            student_data['gpa'] = float(student_data.pop('Not Ortalaması'))
            internships = student_data.pop('Staj Bilgileri (şirket;durasyon)').split(',')
            if len(internships) % 2 != 0:
                raise ValueError("Staj bilgileri çiftler halinde olmalıdır.")
            student_data['internships'] = [{'company': internships[i], 'duration': internships[i+1]} for i in range(0, len(internships), 2)]
            student_data['department'] = student_data.pop('Bölüm')
            return student_data
        except ValueError as ve:
            raise ValueError(f"Girişlerde hata: {ve}")
        except Exception as e:
            raise Exception(f"Veri doğrulanırken hata: {e}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def register_student(self):
        try:
            student_data = self.get_student_data_from_form()
            validated_data = self.validate_student_data(student_data)
            self.system.register_student(validated_data)
            self.clear_form()
            messagebox.showinfo("Başarılı", "Öğrenci kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenci kaydedilirken hata: {e}")

    def update_student(self):
        try:
            student_id = int(self.entries["ID"].get())
            updated_data = self.get_student_data_from_form()
            validated_data = self.validate_student_data(updated_data)
            self.system.update_student_info(student_id, validated_data)
            self.clear_form()
            messagebox.showinfo("Başarılı", "Öğrenci bilgileri güncellendi!")
        except ValueError as ve:
            messagebox.showerror("Hata", f"Girişlerde hata: {ve}")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenci güncellenirken hata: {e}")

    def remove_student(self):
        try:
            student_id = int(self.entries["ID"].get())
            self.system.remove_student(student_id)
            self.clear_form()
            messagebox.showinfo("Başarılı", "Öğrenci silindi!")
        except ValueError as ve:
            messagebox.showerror("Hata", f"Girişlerde hata: {ve}")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenci silinirken hata: {e}")

    def search_student(self):
        try:
            student_id = int(self.search_entry.get())
            student = self.system.search_student(student_id)
            if student:
                student_data = f"ID: {student.student_id}\nAd Soyad: {student.name}\nAdres: {student.address}\nTelefon: {student.phone}\nE-posta: {student.email}\nUyruğu: {student.nationality}\nDoğum Tarihi: {student.birth_date}\nYabancı Dil Seviyesi: {student.foreign_language}\nİlgi Alanları: {', '.join(student.interests)}\nNot Ortalaması: {student.gpa}\nStaj Bilgileri: {', '.join([intern['company'] + ';' + intern['duration'] for intern in student.internships])}\nBölüm: {student.department}"
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, student_data)
            else:
                messagebox.showinfo("Bilgi", "Öğrenci bulunamadı.")
        except ValueError as ve:
            messagebox.showerror("Hata", f"Girişlerde hata: {ve}")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenci aranırken hata: {e}")

    def list_department_students(self):
        try:
            department_name = self.entries["Bölüm"].get()
            students = self.system.list_department_students(department_name)
            if students:
                student_list = tabulate([[student.student_id, student.name, student.department] for student in students], headers=["ID", "Ad Soyad", "Bölüm"])
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, student_list)
            else:
                messagebox.showinfo("Bilgi", "Bu bölümde öğrenci bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenciler listelenirken hata: {e}")

    def list_high_gpa_students(self):
        try:
            students = self.system.list_high_gpa_students()
            if students:
                student_list = tabulate([[student.student_id, student.name, student.gpa] for student in students], headers=["ID", "Ad Soyad", "Not Ortalaması"])
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, student_list)
            else:
                messagebox.showinfo("Bilgi", "Yüksek not ortalamasına sahip öğrenci bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenciler listelenirken hata: {e}")

    def list_advanced_english_students(self):
        try:
            students = self.system.list_advanced_english_students()
            if students:
                student_list = tabulate([[student.student_id, student.name, student.foreign_language] for student in students], headers=["ID", "Ad Soyad", "Yabancı Dil Seviyesi"])
                self.output_box.delete(1.0, tk.END)
                self.output_box.insert(tk.END, student_list)
            else:
                messagebox.showinfo("Bilgi", "İleri seviye İngilizce bilen öğrenci bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Öğrenciler listelenirken hata: {e}")

root = tk.Tk()
app = AlumniSystemApp(root)
root.mainloop()
