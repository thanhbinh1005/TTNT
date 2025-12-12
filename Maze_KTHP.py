import random
import tkinter as tk                     # Import thư viện Tkinter để tạo giao diện GUI
from collections import deque            # Import deque để tạo hàng đợi BFS (rất nhanh)

# ================== Cấu hình ================== #
CELL = 25                                # Kích thước 1 ô vuông trong mê cung (pixel)

# Mê cung dưới dạng ma trận
# 1 = tường, 0 = đường đi, S = điểm bắt đầu, E = điểm kết thúc
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "E", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "S", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "E", 1],
]

HANG = len(MAZE)                         # Số hàng của mê cung
COT = len(MAZE[0])                       # Số cột của mê cung

def random_start_end(maze):
    h = len(maze)
    w = len(maze[0])

    free_cells = [(r, c) for r in range(h) for c in range(w) if maze[r][c] == 0]

    S = random.choice(free_cells)
    free_cells.remove(S)
    E = random.choice(free_cells)

    sr, sc = S
    er, ec = E

    maze[sr][sc] = "S"
    maze[er][ec] = "E"
    return S, E

# ================== Tìm S và E ================== #
def tim_S_E():                           # Hàm tìm vị trí S và E trong mê cung
    S = None                             # Lưu vị trí S
    E = None                             # Lưu vị trí E
    for r in range(HANG):                # Duyệt từng hàng
        for c in range(COT):             # Duyệt từng cột
            if MAZE[r][c] == "S":        # Nếu gặp S
                S = (r, c)               # Lưu tọa độ
            elif MAZE[r][c] == "E":      # Nếu gặp E
                E = (r, c)               # Lưu tọa độ
    return S, E                          # Trả về tuple (S, E)

# Start, End = random_start_end(MAZE)



# ================== Hàm kiểm tra ================== #
def kiemTra(r, c, dong_da_xet):          # Kiểm tra ô (r,c) có thể đi được không
    return (
        0 <= r < HANG and                # Không vượt biên trên/dưới
        0 <= c < COT and                 # Không vượt biên trái/phải
        MAZE[r][c] in (0, "S", "E") and  # Phải là ô hợp lệ
        (r, c) not in dong_da_xet        # Chưa duyệt trước đó
    )


# ================== Truy vết đường đi ================== #
def DUONG_DI(parent, end):               # Dựng lại đường đi từ điểm cuối
    duong = []                           # Mảng lưu các ô của đường đi
    hien_tai = end                       # Bắt đầu từ E
    while hien_tai is not None:          # Lùi dần về S
        duong.append(hien_tai)           # Thêm ô vào danh sách
        hien_tai = parent[hien_tai]      # Lấy "cha" để lùi lại
    duong.reverse()                      # Đảo lại thứ tự từ S → E
    return duong


# ================== GUI + BFS ================== #
class UngDungMaze:                       # Lớp điều khiển ứng dụng chính
    def __init__(self, goc):             # Hàm khởi tạo
        self.goc = goc                   # Lưu cửa sổ chính
        self.goc.title("BFS Maze - DONG / MO")     # Đặt tiêu đề cửa sổ

        self.canvas = tk.Canvas(         # Tạo canvas hiển thị mê cung
            goc,
            width=COT*CELL,              # Chiều rộng
            height=HANG*CELL             # Chiều cao
        )
        self.canvas.pack()               # Hiển thị canvas

        self.label = tk.Label(goc, text="Số ô đã duyệt: 0", font=("Arial", 14)) 
        self.label.pack()

        self.ve_maze()                   # Vẽ mê cung
        self.goc.after(400, self.chay_bfs)   # 0.4 giây sau bắt đầu chạy BFS

    def ve_maze(self):                   # Vẽ toàn bộ mê cung
        for r in range(HANG):            # Duyệt từng hàng
            for c in range(COT):         # Duyệt từng cột
                val = MAZE[r][c]         # Lấy giá trị ô
                if val == 1:             # 1 = tường
                    mau = "black"
                elif val == "S":         # S = xanh lá
                    mau = "green"
                elif val == "E":         # E = đỏ
                    mau = "red"
                else:                    # 0 = trắng
                    mau = "white"
                self.to_mau((r, c), mau) # Tô ô

    def to_mau(self, o, mau):             # Tô 1 ô
        r, c = o                         # Tách ra row/col
        x1, y1 = c*CELL, r*CELL          # Góc trên trái
        x2, y2 = x1 + CELL, y1 + CELL    # Góc dưới phải
        self.canvas.create_rectangle(    # Vẽ hình chữ nhật tương ứng
            x1, y1, x2, y2,
            fill=mau,                    # Màu nền
            outline="gray"               # Khung viền
        )
        self.canvas.update()             # Cập nhật GUI ngay lập tức

    def chay_bfs(self):                  # Hàm thực thi BFS
        mo = deque([Start])              # Hàng đợi mở (các điểm cần duyệt)
        # mo =  [Start]                                                                   #Ngắn xếp
        dong = set()                      # Tập các điểm đã duyệt
        # dong = {Start} 
        parent = {Start: None}           # Lưu cha của mỗi node khi tìm đường

        while mo:                        # Lặp đến khi hết điểm trong hàng đợi
            r, c = mo.popleft()          # Lấy node đầu tiên ra
            # r, c = mo.pop()                                                           #Thử DFS
            dong.add((r, c))             # Đánh dấu đã duyệt

            if MAZE[r][c] not in ("S", "E"):       # Nếu không phải S/E
                self.to_mau((r, c), "lightblue")   # Hiển thị đang duyệt

            self.goc.after(10)           # Tạo hiệu ứng delay

            if (r, c) == End:            # Nếu tìm thấy đích
                break                    # Dừng BFS

            # 4 hướng di chuyển: xuống - lên - phải - trái
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r + dr, c + dc  # Tính tọa độ mới

                if kiemTra(nr, nc, dong) and (nr, nc) not in mo:
                    parent[(nr, nc)] = (r, c)   # Ghi cha của node mới
                    mo.append((nr, nc))        # Đưa node mới vào hàng đợi


        duong = DUONG_DI(parent, End)    # Truy vết đường đi tìm được

        for o in duong:                  # Tô lại đường đi thật
            if MAZE[o[0]][o[1]] not in ("S", "E"):
                self.to_mau(o, "yellow") # Tô vàng cho đường đi
            self.goc.after(50)           # Thêm hiệu ứng
        print("Số lượng ô đã duyệt",len(dong))
        self.label.config(text=f"Số ô đã duyệt: {len(dong)}")  #hiển thị số lượng ô đã đi qua


# ================== Chạy ứng dụng ================== #
if __name__ == "__main__":               # Chỉ chạy nếu chạy trực tiếp file
    Start, End = tim_S_E()               # Gọi hàm và nhận vị trí bắt đầu/kết thúc
    goc = tk.Tk()                        # Tạo cửa sổ giao diện
    ung_dung = UngDungMaze(goc)          # Khởi tạo ứng dụng
    goc.mainloop()                       # Vòng lặp giao diện

# maze = [  
#    [ 1, "S", 0, 0, 0, 0],
#    [ 1, 0, 1, 0, 1, 1],
#    [ 1, 0, 0, 1, 1, 1],
#    [ 1, 1, 0, 1, 1, 0],
#    [ "E", 0, 0, 0, 1, 0],
#    [ 1, 1, 1, 1, 0, 0]
# ]