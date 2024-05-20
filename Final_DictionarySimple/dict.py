import tkinter as tk
from tkinter import messagebox
#pip install tk

class TrieNode:
    def __init__(self):
        self.child = {}
        self.is_end_of_word = False
        self.translations = []

All_of_words = []
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, translation: str):


        #Hàm insert đưa các từ vào trong cây trie

        word = word.lower()  # Chuẩn hóa từ
        node = self.root
        for char in word:
            if char not in node.child:
                node.child[char] = TrieNode()   #Nếu chưa có ký tự hiện tại trong các nút con của node thì ta tạo một trienode mới
            node = node.child[char]
        if node.is_end_of_word != True: 
            All_of_words.append((word,translation))

        node.is_end_of_word = True    #Đánh dấu kết thúc của từ
        node.translations.append(translation) #giúp một từ có thể có nhiều nghĩa

    def search(self, word: str) -> list:
        word = word.lower()  # Chuẩn hóa từ
        node = self.root
        for char in word:
            if char not in node.child:
                return []    #Nếu không có ký tự hiện tại trong các nút con của node thì tức là không tồn tại từ này
            node = node.child[char]
        return node.translations if node.is_end_of_word else [] #Nếu node được đánh dấu là kết của một từ thì ta trả về từ đó không thì rỗng
    
    def _find_words_with_prefix(self, node, prefix, words, len):
        if len == 3: return
        if node.is_end_of_word:  #Nếu node này được đánh dấu là node của một từ thì ta thêm từ đó vô words
            words.append((prefix, node.translations))


        for char, child_node in node.child.items():
            """
            Đệ quy gọi hàm _find_words_with_prefix trên mỗi node con, với prefix được cập nhật bằng cách thêm ký tự char và words 
            là danh sách các từ được tìm thấy. Điều này giúp duyệt sâu vào cấu trúc Trie để tìm các từ có tiền tố là prefix.
            """
            self._find_words_with_prefix(child_node, prefix + char, words,len+1)
    
    def find_same_words(self, prefix: str) -> list:

        prefix = prefix.lower()  # Chuẩn hóa từ
        node = self.root
        tmp = ""
        TP = []
        if len(prefix) <= 2: tmp = prefix
        else:
            for i in range(len(prefix)-1):  
                tmp = tmp + prefix[i] 
        tam = ""
        for char in tmp:
            tam = tam + char
            if char not in node.child:
                return TP  # Trả về danh sách 
            node = node.child[char]
            if node.is_end_of_word == True:
                TP.append((tam,node.translations))
        # Sử dụng tmp để tìm từ có tiền tố giống tmp
        
        self._find_words_with_prefix(node, tmp, TP,0)

        words = []
        #Loại bỏ prefix khỏi list để không in ra chính từ đó
        for word,trans in TP:
            if not word == prefix:
                words.append((word,trans))

        return words
                            

    

class DictionaryApp:
    def __init__(self, root, vocabulary_file_en, vocabulary_file_vi, insertEn, insertVi):

        """
        Trước hết đây là chức năng của một số lớp thuộc thư viện tkinter mà em sẽ dùng :
        tk.Label : Được sử dụng để tạo nhãn (label) trong giao diện người dùng.
        tk.OptionMenu : Được sử dụng để tạo một menu chọn có thể chứa một danh sách các tùy chọn.
        tk.Entry : Được sử dụng để tạo một ô nhập liệu cho người dùng có thể nhập văn bản hoặc dữ liệu khác.
        tk.Button : Được sử dụng để tạo một nút trong giao diện người dùng để thực hiện các hành động hoặc chức năng nhất định khi người dùng nhấp vào nút đó.
        tk.Text : Được sử dụng để tạo một ô văn bản đa dòng trong giao diện người dùng. Ô văn bản này cho phép hiển thị và chỉnh sửa văn bản có thể được cuộn.
        widget.get() : Được sử dụng để lấy nội dung hiện tại của một widget trong tkinter, chẳng hạn như Entry hoặc Text. 
                       Khi được gọi, phương thức này trả về chuỗi đại diện cho nội dung hiện tại của widget.
        widget.delete() : Được sử dụng trong các widget của thư viện tkinter để xóa nội dung của widget đó.
        messagebox.showinfo(...) : được sử dụng để hiển thị một hộp thoại thông báo với một tin nhắn thông tin.
        messagebox.showwarning(...) : được sử dụng để hiển thị một hộp thoại cảnh báo (warning dialog) cho người dùng.
        """

        self.trie_en = Trie() #Cây trie cho tiếng anh
        self.trie_vi = Trie() #Cây trie cho tiếng việt
        self.root = root
        self.root.title("Đồ án từ điển")
        

        #Tạo một biến loại stringvar để lưu trữ loại từ điển
        self.typdict = tk.StringVar()
        self.typdict.set("English-Vietnamese")

        
        
        #Tạo một menu cho phép chọn giữa từ diển anh anh và anh việt
    
        self.type = tk.Label(root, text="Loại từ điển:")
        self.type.grid(row=0, column=0, padx=10, pady=10)
        self.menu = tk.OptionMenu(root, self.typdict, "English-English", "English-Vietnamese", command=self.loadVocab)
        self.menu.grid(row=0, column=1, padx=10, pady=10)
        

        #Tạo 2 ô nhập liệu(entry) để nhập từ với mong muốn thêm những từ cá nhân vào trong từ điển 
        self.tu = tk.Label(root, text="Từ:")
        self.tu.grid(row=1, column=0, padx=10, pady=10)
        self.nhaptu = tk.Entry(root)
        self.nhaptu.grid(row=1, column=1, padx=10, pady=10)
        
        self.translation = tk.Label(root, text="Dịch nghĩa:")
        self.translation.grid(row=2, column=0, padx=10, pady=10)
        self.nhapnghia = tk.Entry(root)
        self.nhapnghia.grid(row=2, column=1, padx=10, pady=10)

        #2 button giúp thêm và xóa các từ được người dùng đóng góp
        self.themtu = tk.Button(root, text="Thêm", command=self.insertWord)
        self.themtu.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.xoatu = tk.Button(root, text="Reset", command=self.resetFiles)
        self.xoatu.grid(row=4, column=0, columnspan=2, pady=10)
        

        #Tạo ô tra từ điển và nút tra từ
        self.searchword = tk.Label(root, text="Từ cần tra:")
        self.searchword.grid(row=5, column=0, padx=10, pady=10)
        self.tratu = tk.Entry(root)
        self.tratu.grid(row=5, column=1, padx=10, pady=10)
        
        self.search_button = tk.Button(root, text="Tra", command=self.searchWord)
        self.search_button.grid(row=6, column=0, columnspan=2, pady=10)
        
    
        #Tạo ô kết quả
        self.kq = tk.Label(root, text="Kết quả tìm kiếm")
        self.kq.grid(row=7, column=0, padx=10, pady=10)

        self.ketqua = tk.Text(root, height=10, width = 70)
        self.ketqua.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        #Tạo ô những từ gần giống từ cần tìm
        self.giong = tk.Button(root, text="Một số từ giống với từ của bạn:", command=self.sameWord)
        self.giong.grid(row=9, column=0, padx=10, pady=10)
        self.same = tk.Text(root, height=15, width=70)
        self.same.grid(row=10, column=0, columnspan=2, padx=10, pady=10)


        self.vocabulary_file_en = vocabulary_file_en
        self.vocabulary_file_vi = vocabulary_file_vi
        self.insertEn = insertEn
        self.insertVi = insertVi
        self.loadVocab()

    def loadVocab(self, *args):
        """
        Vai trò tải từ vựng từ file vào Trie tương ứng.
        Các biến vocabulary_file,insert_file và trie sẽ phụ thuộc vào loại từ điển nào
        """
        if self.typdict.get() == "English-English":  
            vocabulary_file = self.vocabulary_file_en   
            insert_file = self.insertEn
            trie = self.trie_en
        else:
            vocabulary_file = self.vocabulary_file_vi
            insert_file = self.insertVi
            trie = self.trie_vi

        trie.root = TrieNode()  # Reset Trie
        for file_path in [vocabulary_file, insert_file]:
            with open(file_path, "r", encoding="utf-8") as file: #mở file ở chế độ đọc "r" và định dạng utf 8 vì utf 8 hỗ trợ tiếng việt
                for line in file: #duyệt qua từng dòng
                    if ":" in line: 
                        # Sử dụng dấu hai chấm ":" làm điểm chia. Phần split(":", 1) sẽ tách chuỗi thành 2 phần, chỉ tách ở dấu ":" đầu tiên tìm thấy.
                        word, translation = line.strip().split(":", 1) 
                        # Ta thêm từ đó vào trie, phương thức strip giúp loại bỏ các khoảng trắng thừa
                        trie.insert(word.strip(), translation.strip())

    def insertWord(self):
        word = self.nhaptu.get()  #Lấy từ trong ô nhập liệu từ
        translation = self.nhapnghia.get() #Lấy từ trong ô nhập liệu nghĩa
        if word and translation: #Nếu đã nhập đủ cả từ và nghĩa
            if self.typdict.get() == "English-English": 
                self.trie_en.insert(self.root,word, translation)  #Thêm vào cây trie tiếng anh
                with open(self.insertEn, "a", encoding="utf-8") as file:
                    file.write(f"{word}: {translation}\n")    #Mở file insert_en và ghi từ vừa nhập vào
            else:
                self.trie_vi.insert(word, translation)  #Thêm vào cây trie tiếng việt
                with open(self.insertVi, "a", encoding="utf-8") as file:
                    file.write(f"{word}: {translation}\n") #Mở file insert_vi và ghi từ vừa nhập vào
            messagebox.showinfo("Thành công", f"Đã thêm '{word}' với dịch nghĩa '{translation}'.")
        else:
            messagebox.showwarning("Lỗi nhập", "Vui lòng nhập cả từ và dịch nghĩa.")
        self.nhaptu.delete(0, tk.END) #Xóa nội dung trong ô nhập liệu từ
        self.nhapnghia.delete(0, tk.END) #Xóa nội dung trong ô nhập liệu chữ

    def resetFiles(self):
        if self.typdict.get() == "English-English":  #Nếu đang là tử điển tiếng anh 
            with open(self.insertEn, "w", encoding="utf-8"): #Mở file insert tiếng Anh (self.insertEn) trong chế độ ghi (write mode). 
                self.loadVocab() #Ta load lại từ vựng
            messagebox.showinfo("Thành công", "Đã reset file insert tiếng Anh.")
        elif self.typdict.get() == "English-Vietnamese": #Nếu đang là tử điển tiếng việt
            with open(self.insertVi, "w", encoding="utf-8"): #Mở file insert tiếng Việt (self.insertEn) trong chế độ ghi (write mode).
                self.loadVocab()  #Ta load lại từ vựng
            messagebox.showinfo("Thành công", "Đã reset file insert tiếng Việt.")


    def searchWord(self):
        #Vai trò : Tìm kiếm từ
        word = self.tratu.get() #Lấy từ trong ô nhập liệu
        if self.typdict.get() == "English-English":
            translations = self.trie_en.search(word)    #Tìm kiếm trong cây trie tiếng anh
        else:
            translations = self.trie_vi.search(word) #Tìm kiếm trong cây trie tiếng việt
        
        self.ketqua.delete(1.0, tk.END) #xóa dữ liệu trong ô kết quả
        if translations:
            result = f"Từ cần tìm: {word}\nÝ nghĩa: {', '.join(translations)}\n\n"
        else:
            result = f"Từ cần tìm: {word}\nÝ nghĩa: Không tìm thấy\n\n"
        
        self.ketqua.insert(tk.END, result) #Thêm dữ liệu result vô ô kết quả

    def sameWord(self):
        #Vai trò : Tìm kiếm từ
        word = self.tratu.get() #Lấy từ trong ô nhập liệu
        if self.typdict.get() == "English-English":
            words = self.trie_en.find_same_words(word)    #Tìm kiếm trong cây trie tiếng anh
        else:
            words = self.trie_vi.find_same_words(word) #Tìm kiếm trong cây trie tiếng việt
        
        self.same.delete(1.0, tk.END) #xóa dữ liệu trong ô kết quả
        
        if words:
            result = "Những từ có thể giống với từ bạn vừa nhập:\n"
            for prefix_word, prefix_translations in words:
                result += f"{prefix_word}: {', '.join(prefix_translations)}\n"
        else:
            result = "Không tìm thấy từ nào giống với từ bạn vừa nhập.\n"
        
        self.same.delete(1.0, tk.END)
        self.same.insert(tk.END, result) #Thêm dữ liệu result vô ô kết quả




if __name__ == "__main__":
    root = tk.Tk()
    vocabulary_file_en = "vocabEn.txt"  # Đường dẫn tới file từ vựng Anh
    vocabulary_file_vi = "vocabVi.txt"  # Đường dẫn tới file từ vựng Việt
    insertEn = "insertEn.txt"  # Đường dẫn tới file insert từ vựng Anh
    insertVi = "insertVi.txt"  # Đường dẫn tới file insert từ vựng Việt
    app = DictionaryApp(root, vocabulary_file_en, vocabulary_file_vi, insertEn, insertVi)
    root.mainloop()