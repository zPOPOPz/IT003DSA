import tkinter as tk
from tkinter import messagebox

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
    
    def _findWordsWithPrefix(self, node: TrieNode, prefix: str, suggestions: list):
        """
        Phương thức hỗ trợ tìm kiếm các từ có tiền tố giống với từ được nhập.
        """
        if node.is_end_of_word:
            suggestions.append(prefix)
        
        for char, child_node in node.child.items():
            self._findWordsWithPrefix(child_node, prefix + char, suggestions)
    
    def findWordsWithPrefix(self, prefix: str) -> list:
        prefix = prefix.lower()  # Chuẩn hóa từ
        node = self.root
        suggestions = []
        for char in prefix:
            if char not in node.child:
                return []    #Nếu không có ký tự hiện tại trong các nút con của node thì tức là không tồn tại từ này
            node = node.child[char]
        self._findWordsWithPrefix(node, prefix, suggestions)
        return suggestions

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
        self.search_history = []
        self.root.title("Đồ án từ điển")
        
        #Tạo một biến loại stringvar để lưu trữ loại từ điển
        self.typdict = tk.StringVar()
        self.typdict.set("English-Vietnamese")

        #Tạo một menu cho phép chọn giữa từ diển anh anh và anh việt
        self.type = tk.Label(root, text="Loại từ điển:")
        self.type.grid(row=0, column=0, padx=10, pady=10)
        self.menu = tk.OptionMenu(root, self.typdict, "English-English", "English-Vietnamese", command=self.loadVocab)
        self.menu.grid(row=0, column=1, padx=10, pady=10)
        
        #Tạo 3 ô nhập liệu(entry) để nhập từ với mong muốn thêm những từ cá nhân vào trong từ điển 
        self.Them = tk.Label(root, text = "Đóng góp từ vựng:")
        self.Them.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.tu = tk.Label(root, text="Từ:")
        self.tu.grid(row=2, column=0, padx=10, pady=10)
        self.nhaptu = tk.Entry(root)
        self.nhaptu.grid(row=2, column=1, padx=10, pady=10)
        
        self.pronounce = tk.Label(root, text = "Phiên âm:")
        self.pronounce.grid(row=3, column=0,padx=10,pady=10)
        self.phienam = tk.Entry(root)
        self.phienam.grid(row=3,column=1,padx=10,pady=10)

        self.translation = tk.Label(root, text="Dịch nghĩa:")
        self.translation.grid(row=4, column=0, padx=10, pady=10)
        self.nhapnghia = tk.Entry(root)
        self.nhapnghia.grid(row=4, column=1, padx=10, pady=10)

        #2 button giúp thêm và xóa các từ được người dùng đóng góp
        self.themtu = tk.Button(root, text="Thêm", command=self.insertWord)
        self.themtu.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.xoatu = tk.Button(root, text="Reset", command=self.resetFiles)
        self.xoatu.grid(row=6, column=0, columnspan=2, pady=10)
        
        #Tạo ô tra từ điển và nút tra từ
        self.searchword = tk.Label(root, text="Từ cần tra:")
        self.searchword.grid(row=7, column=0, padx=10, pady=10)
        self.tratu = tk.Entry(root)
        self.tratu.grid(row=7, column=1, padx=10, pady=10)
        self.tratu.bind("<KeyRelease>", self.suggestWords)  # Kích hoạt gợi ý từ khi nhập liệu
        
        self.search_button = tk.Button(root, text="Tra🔍", command=self.searchWord)
        self.search_button.grid(row=8, column=0, columnspan=2, pady=10)
        # Tạo nút hoặc biểu tượng để thêm từ yêu thích
        self.add_favorite_button = tk.Button(root, text="❤️", command=self.addToFavorites)
        self.add_favorite_button.grid(row=8, column=1, padx=10, pady=10)
        #Tạo ô kết quả
        self.kq = tk.Label(root, text="Kết quả tìm kiếm")
        self.kq.grid(row=9, column=0, padx=10, pady=10)
        self.ketqua = tk.Text(root, height=10, width = 70)
        self.ketqua.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.history_button = tk.Button(root, text="Lịch sử tìm kiếm ↺", command=self.displaySearchHistory)
        self.history_button.grid(row=11, column=0, columnspan=2, pady=10)

        self.vocabulary_file_en = vocabulary_file_en
        self.vocabulary_file_vi = vocabulary_file_vi
        self.insertEn = insertEn
        self.insertVi = insertVi
        self.loadVocab()

        # Khởi tạo danh sách từ yêu thích
        self.favorite_words = set()

        # Tạo nút hoặc biểu tượng để mở cửa sổ danh sách từ yêu thích
        self.favorites_window_button = tk.Button(root, text="Danh sách từ yêu thích❤️ ", command=self.openFavoritesWindow)
        self.favorites_window_button.grid(row=12, column=0, columnspan=2, pady=10)

        # Khởi tạo cửa sổ danh sách từ yêu thích
        self.favorites_window = None
    

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
        prono = self.phienam.get() #Lấy từ trong ô phiên âm
        translation = self.nhapnghia.get() #Lấy từ trong ô nhập liệu nghĩa
        if word and translation and prono: #Nếu đã nhập đủ cả từ và nghĩa
            if self.typdict.get() == "English-English":
                prono = "/" + prono + "/"
                self.trie_en.insert(word,prono) #Thêm phát âm 
                self.trie_en.insert(word, translation)  #Thêm vào cây trie tiếng anh
                with open(self.insertEn, "a", encoding="utf-8") as file:
                    file.write(f"{word}: {translation}\n")    #Mở file insert_en và ghi từ vừa nhập vào
            else:
                prono = "/" + prono + "/"
                self.trie_vi.insert(word,prono)
                self.trie_vi.insert(word, translation)  #Thêm vào cây trie tiếng việt
                with open(self.insertVi, "a", encoding="utf-8") as file:
                    file.write(f"{word}: {translation}\n") #Mở file insert_vi và ghi từ vừa nhập vào
            messagebox.showinfo("Thành công", f"Đã thêm '{word}' với dịch nghĩa '{translation}'.")
        else:
            messagebox.showwarning("Lỗi nhập", "Vui lòng nhập cả từ và dịch nghĩa.")
        self.nhaptu.delete(0, tk.END) #Xóa nội dung trong ô nhập liệu từ
        self.nhapnghia.delete(0, tk.END) #Xóa nội dung trong ô nhập liệu chữ
        self.phienam.delete(0,tk.END)

    def resetFiles(self):
        if self.typdict.get() == "English-English":  #Nếu đang là tử điển tiếng anh 
            with open(self.insertEn, "w", encoding="utf-8"): #Mở file insert tiếng Anh (self.insertEn) trong chế độ ghi (write mode). 
                self.loadVocab() #Ta load lại từ vựng
            messagebox.showinfo("Thành công", "Đã reset file insert tiếng Anh.")
        elif self.typdict.get() == "English-Vietnamese": #Nếu đang là tử điển tiếng việt
            with open(self.insertVi, "w", encoding="utf-8"): #Mở file insert tiếng Việt (self.insertEn) trong chế độ ghi (write mode).
                self.loadVocab()  #Ta load lại từ vựng
            messagebox.showinfo("Thành công", "Đã reset file insert tiếng Việt.")

    def suggestWords(self, event):
        """
        Hàm gợi ý các từ có tiền tố giống với từ được nhập.
        """
        prefix = self.tratu.get()
        if self.typdict.get() == "English-English":
            suggestions = self.trie_en.findWordsWithPrefix(prefix)
        else:
            suggestions = self.trie_vi.findWordsWithPrefix(prefix)
        
        self.ketqua.delete(1.0, tk.END)
        if suggestions:
            result = f"Gợi ý cho '{prefix}':\n"
            for suggestion in suggestions:
                result += suggestion + '\n'
        else:
            result = f"Không có gợi ý cho '{prefix}'.\n"
        
        self.ketqua.insert(tk.END, result)

    def searchWord(self):
        word = self.tratu.get() #Lấy từ trong ô nhập liệu
        if self.typdict.get() == "English-English":
            translations = self.trie_en.search(word)    #Tìm kiếm trong cây trie tiếng anh
        else:
            translations = self.trie_vi.search(word) #Tìm kiếm trong cây trie tiếng việt
        
        self.ketqua.delete(1.0, tk.END) #xóa dữ liệu trong ô kết quả
        if translations:
            result = f"Từ cần tìm: {word}\n"
            result += f"Phát âm: {translations[0]}\n"
            del translations[0]
            result += "Ý Nghĩa:\n"
            for st in translations:
                result = result + st + '\n'
        else:
            result = f"Từ cần tìm: {word}\nÝ nghĩa: Không tìm thấy\n\n"

        self.updateSearchHistory(word) #Thêm từ cần tìm vào ô kết quả

        self.ketqua.insert(tk.END, result) #Thêm dữ liệu result vô ô kết quả
    

    def updateSearchHistory(self, word):
        # Thêm từ đã tìm kiếm vào lịch sử và giới hạn số lượng mục trong lịch sử
        self.search_history.insert(0, word)
        self.search_history = self.search_history[:10]  # Giới hạn lịch sử tìm kiếm chỉ chứa tối đa 10 mục

    def displaySearchHistory(self):
        # Hiển thị danh sách lịch sử trong một cửa sổ mới hoặc trong cùng cửa sổ chính của ứng dụng
        history_window = tk.Toplevel(self.root)
        history_window.title("Lịch sử tìm kiếm")

        history_label = tk.Label(history_window, text="Lịch sử tìm kiếm:")
        history_label.pack()

        history_listbox = tk.Listbox(history_window)
        for word in self.search_history:
            history_listbox.insert(tk.END, word)
        history_listbox.pack()

        close_button = tk.Button(history_window, text="Đóng", command=history_window.destroy)
        close_button.pack()

    def openFavoritesWindow(self):
        self.favorites_window = tk.Toplevel(self.root)
        self.favorites_window.title("Danh sách từ yêu thích")
        self.favorites_listbox = tk.Listbox(self.favorites_window, height=10, width=50)
        self.favorites_listbox.pack(padx=10, pady=10)

        # Hiển thị danh sách từ yêu thích trong danh sách
        for word in self.favorite_words:
            self.favorites_listbox.insert(tk.END, word)

    def removeFromFavorites(self, event):
        selected_index = self.favorites_listbox.curselection()
        if selected_index:
            word = self.favorites_listbox.get(selected_index)
            self.favorite_words.remove(word)
            self.favorites_listbox.delete(selected_index)
            messagebox.showinfo("Thông báo", f"Từ '{word}' đã được loại khỏi danh sách yêu thích.")
    def addToFavorites(self):
        word = self.tratu.get() #Lấy từ trong ô nhập liệu
        if word:
            if word in self.favorite_words:
                self.favorite_words.remove(word)
                messagebox.showinfo("Thông báo", f"Từ '{word}' đã được xóa khỏi danh sách yêu thích.")
            else:
                self.favorite_words.add(word)
                messagebox.showinfo("Thông báo", f"Từ '{word}' đã được thêm vào danh sách yêu thích.")

if __name__ == "__main__":
    root = tk.Tk()
    vocabulary_file_en = "vocabEn.txt"  # Đường dẫn tới file từ vựng Anh
    vocabulary_file_vi = "vocabVi.txt"  # Đường dẫn tới file từ vựng Việt
    insertEn = "insertEn.txt"  # Đường dẫn tới file insert từ vựng Anh
    insertVi = "insertVi.txt"  # Đường dẫn tới file insert từ vựng Việt
    app = DictionaryApp(root, vocabulary_file_en, vocabulary_file_vi, insertEn, insertVi)
    root.mainloop()