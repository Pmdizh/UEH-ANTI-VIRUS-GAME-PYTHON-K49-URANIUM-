import pygame, sys#cung cấp cho chương trình Python truy cập vào các thông tin và chức năng liên quan đến chính chương trình Python #
import os#cung cấp cho lập trình viên quyền truy cập vào các chức năng hệ điều hành. Module os cung cấp nhiều hàm và biến để tương tác với hệ điều hành,#
import random

player_lives = 3                                                # số mạng
score = 0                                                       # số điểm
viruss = ['Morris', 'Melissa', 'Nimda', 'Klez', 'bomb', 'increase', 'decrease']    #các loại vật phẩm xuất hiện
increased_speed = 50  # Giả sử tốc độ tăng là 5
decreased_speed = -50  # Giả sử tốc độ giảm là -5
high_score = 0 


# tạo cửa sổ trò chơi
WIDTH = 800
HEIGHT = 500
FPS = 10                                                 # thiết lập tần số màng hình
pygame.init()    #là câu lệnh khởi tạo thư viện Pygame, dislay quản lí hình ảnh trong 
pygame.display.set_caption('UEH Anti Virus Game in Python -- GetProjects.org') #set_caption(): Là một hàm trong mô-đun pygame.display, dùng để thiết lập tiêu đề cho cửa sổ trò chơi
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #tạo ra cửa sổ trò chơi và gán nó vào biến gameDisplay
clock = pygame.time.Clock() # tạo ra một đối tượng đồng hồ (clock) giúp kiểm soát tốc độ khung hình (framerate) của trò chơi.

# Định nghĩa màu
WHITE = (255,255,255) 
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Cài đặt âm thanh và nhạc
pygame.mixer.init()
pygame.mixer.music.load("nhac_nen.mp3")  # Đặt tên file nhạc nền của bạn
pygame.mixer.music.set_volume(0.5)  # Đặt âm lượng (từ 0.0 đến 1.0)
pygame.mixer.music.play(-1)  # -1 để phát lại vô hạn, 0 để phát một lần
sound_effect = pygame.mixer.Sound("nhac_game.mp3")  # Âm thanh khi trò chơi bắt đầu
sound_effect.set_volume(0.8)



background = pygame.image.load('back.jpg')       # gán hình ảnh có tên back vào biến background , load tải ảnh
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42) #tạo ra một đối tượng font chữ với tên font là "comic.ttf" và cỡ chữ 42.
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    # kiểu chữ điểm số 
#Thông số truyền vào:
'''Score : ' + str(score): Chuỗi văn bản muốn hiển thị, bao gồm văn bản tĩnh "Score :" và giá trị điểm số được chuyển đổi thành chuỗi (str(score)).
True: Bật chế độ chống răng cưa (anti-aliasing) cho văn bản, giúp các cạnh của văn bản trông mịn hơn.
(255, 255, 255): Màu sắc của văn bản, trong trường hợp này là màu trắng.'''
lives_icon = pygame.image.load('images/white_lives.png')   # tải hình ảnh lives từ white_lives và gán vào lives_icon


def generate_random_viruss(virus): # tạo hàm radom viruss
    global loop_count
    global bomb_count
    virus_path = "images/" + virus + ".png" #Tạo một đường dẫn đến hình ảnh của trái cây dựa trên tên của trái cây và đặt nó vào biến 
    data[virus] = {#Tạo một entry mới trong dictionary data với key là virus
        'img': pygame.image.load(virus_path), # load hình ảnh từ virus_path
        'x' : random.randint(100,500),   # giá trị của x nằm ngẫu nhiên trong 100 đến 500       
        'y' : 800, #giá trị cố định của y là 800
        'speed_x': random.randint(-10,10),      # Xác định tốc độ di chuyển theo trục x của trái cây, là một số ngẫu nhiên trong khoảng từ -10 đến 10.
        'speed_y': random.randint(-80, -60),    #Xác định tốc độ di chuyển theo trục y của trái cây, là một số ngẫu nhiên trong khoảng từ -80 đến -60. Âm nghĩa là di chuyển lên trên.
        'throw': False,                         #Ban đầu đặt trạng thái ném ('throw') của trái cây là False.
        't': 0,                                 #: Khởi tạo giá trị thời gian ('t') là 0
        'hit': False,                           # Ban đầu đặt trạng thái va chạm ('hit') của trái cây là False.
    }
    if random.random() >= 0.75:     #: Kiểm tra xác suất để quyết định trái cây có nên được ném ra khỏi màn hình hay không. Nếu số ngẫu nhiên lớn hơn hoặc bằng 0.75, 
        #Hàm này trả về một số ngẫu nhiên trong khoảng từ 0 đến 1 (bao gồm 0, nhưng không bao gồm 1).
        data[virus]['throw'] = True #đặt giá trị của thuộc tính 'throw' của trái cây (được định nghĩa trong dictionary data với key là virus) là True. Điều này có thể được hiểu là trái cây sẽ được "ném" ra khỏi màn hình.
    else:
        data[virus]['throw'] = False #Nếu điều kiện sai, đặt giá trị của thuộc tính 'throw' của trái cây là False. Điều này có thể được hiểu là trái cây sẽ không được "ném" ra khỏi màn hình.

# Dictionary to hold the data the random virus generation
data = {}
for virus in viruss: # vòng lập 
    generate_random_viruss(virus) # random virus từ các loại viruss

def hide_cross_lives(x, y): # tạo hàm chức năng thể hiện số mạng sống nhận 2 thông số x và y là tọa độ xuất hiện trên màng hình 
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))# Tải hình ảnh từ đường dẫn "images/red_lives.png". Hình ảnh này được đặt trong hàm pygame.image.load và sẽ được sử dụng để vẽ lên màn hình.

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')#Xác định tên của font chữ mà bạn muốn sử dụng, hàm match_font để tìm font chữ phù hợp với tên 'comic.ttf'.
def draw_text(display, text, size, x, y):#Định nghĩa hàm có tên là draw_text với các tham số là display (màn hình), text (chuỗi văn bản cần vẽ), size (kích thước của font), x và y (tọa độ trên màn hình).
    font = pygame.font.Font(font_name, size)#Tạo một đối tượng font từ tên font và kích thước được chỉ định. Điều này sẽ được sử dụng để vẽ văn bản.
    text_surface = font.render(text, True, GREEN)# sử dụng phương thức render của đối tượng font. Bề mặt này sẽ chứa văn bản được vẽ, có màu trắng (WHITE). Tham số thứ hai là chế độ antialiasing (True có nghĩa là bật chế độ antialiasing).
    text_rect = text_surface.get_rect()#Tạo một hình chữ nhật (rect) chứa văn bản. Đối tượng rect này được sử dụng để đặt vị trí của văn bản trên màn hình.
    text_rect.midtop = (x, y)#. Điều này có nghĩa là vị trí chính giữa trên cùng của hình chữ nhật sẽ được đặt tại tọa độ (x, y).
    gameDisplay.blit(text_surface, text_rect)# Sử dụng phương thức blit để vẽ bề mặt văn bản (text_surface) lên màn hình tại vị trí được xác định bởi hình chữ nhật (text_rect).



# một hàm trong Python sử dụng thư viện Pygame để vẽ các biểu tượng số lượng "mạng sống" (lives) lên màn hình trò chơi.
def draw_lives(display, x, y, lives, image) :
    '''Định nghĩa hàm có tên là draw_lives nhận các tham số sau:
    

display: đối tượng màn hình Pygame.
x: tọa độ x (hoành độ) của vị trí bắt đầu vẽ các biểu tượng "mạng sống".
y: tọa độ y (tung độ) của vị trí bắt đầu vẽ các biểu tượng "mạng sống".
lives: số lượng "mạng sống" cần vẽ.
image: đường dẫn của hình ảnh biểu tượng "mạng sống".'''

    for i in range(lives) :#Dùng vòng lặp for để lặp qua số lượng "mạng sống" cần vẽ (biểu tượng "mạng sống").
        img = pygame.image.load(image)  #Tải hình ảnh của biểu tượng "mạng sống" từ đường dẫn được truyền vào.
        img_rect = img.get_rect()       #Lấy hình chữ nhật (rect) chứa biểu tượng "mạng sống". Rect này sẽ được sử dụng để đặt vị trí và kích thước của hình ảnh.
        img_rect.x = int(x + 35 * i)    #Đặt tọa độ x của hình chữ nhật chứa biểu tượng "mạng sống" sao cho nó cách nhau 35 pixel, và được dịch chuyển về phải dựa trên giá trị của i.
        img_rect.y = y                  #Đặt tọa độ y của hình chữ nhật chứa biểu tượng "mạng sống" theo giá trị của y.
        display.blit(img, img_rect)     # Sử dụng phương thức blit để vẽ hình ảnh biểu tượng "mạng sống" lên màn hình tại vị trí được xác định bởi hình chữ nhật 

# định nghĩa 1 hàm trong Python sử dụng thư viện Pygame để hiển thị màn hình game over
def show_gameover_screen():
    gameDisplay.blit(background, (0,0))#Sử dụng phương thức blit để vẽ hình nền của màn hình game over lên gameDisplay. Đối số đầu tiên là hình nền (background), và đối số thứ hai là tọa độ (0,0) đặt hình nền ở góc trái trên của màn hình.
    draw_text(gameDisplay, "UEH ANTI VIRUS", 90, WIDTH / 2, HEIGHT / 4) # gọi  hàm draw_text đã đc dịnh nghĩa ơ tr , ghi chữ virus ninja  với kích thước font là 90, tại vị trí nằm giữa chiều rộng và chiều cao của màn hình (tức là WIDTH / 2 và HEIGHT / 4).
    pygame.mixer.music.stop()

    # Phát lại nhạc nền khi trò chơi kết thúc
    pygame.mixer.music.load("nhac_nen.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    if not game_over : 
        draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)# Kiểm tra biến game_over. Nếu trò chơi chưa kết thúc (not game_over), thì vẽ điểm số lên màn hình bằng cách gọi hàm draw_text với văn bản là "Score : " cộng với giá trị của biến score, kích thước font là 50, và vị trí ở giữa chiều rộng và chiều cao (WIDTH / 2 và HEIGHT / 2).
        draw_text(gameDisplay,"HighScore : " + str(high_score), 50, WIDTH / 2, HEIGHT /2.5)
    draw_text(gameDisplay, "CLICK TO START ", 64, WIDTH / 2, HEIGHT * 3 / 4) #Vẽ văn bản "Press a key to begin!" với kích thước font là 64, tại vị trí ở giữa chiều rộng và chiều cao, nhưng nằm ở 3/4 chiều cao (WIDTH / 2 và HEIGHT * 3 / 4).
    pygame.display.flip() #Cập nhật toàn bộ màn hình để hiển thị các thay đổi đã được thực hiện trước đó.
    waiting = True #Tạo một biến waiting và gán giá trị là True. Biến này sẽ kiểm soát việc chờ đợi người chơi nhấn một phím để bắt đầu trò chơi mới.
    while waiting: #Bắt đầu một vòng lặp vô hạn để chờ đợi người chơi nhấn một phím.
        clock.tick(FPS) #diều này giữ cho vòng lặp chờ đợi chạy với tốc độ không quá FPS khung hình mỗi giây, để tránh việc vòng lặp chạy quá nhanh.
        for event in pygame.event.get():#Lặp qua tất cả các sự kiện Pygame trong hàng đợi sự kiện.
            if event.type == pygame.QUIT:
                pygame.quit()#Nếu người chơi nhấn nút đóng cửa sổ, sự kiện QUIT được kích hoạt, và trò chơi sẽ kết thúc bằng cách gọi 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.load("nhac_game.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                waiting = False #Nếu người chơi nhấn một phím (sự kiện KEYUP), biến waiting được đặt thành False, và vòng lặp chờ đợi sẽ kết thúc.

last_speed_change_time = pygame.time.get_ticks()#khai báo biến để theo dõi thời điểm mà tốc độ sẽ được thay đổi:
# Vòng lập trò chơi( vòng lập chính của trò chơi)
                
first_round = True      # Được sử dụng để kiểm soát việc hiển thị màn hình game over chỉ trong vòng lặp đầu tiên.
game_over = True        # Chấm dứt vòng lặp chính nếu có nhiều hơn 3 quả bom được chọn.
game_running = True     # Quản lý vòng lặp chính của trò chơi.
while game_running :    #Bắt đầu vòng lặp chính của trò chơi. Vòng lặp sẽ tiếp tục khi game_running là True.
    if game_over :
        if first_round : #Điều kiện này kiểm tra xem có phải là vòng lặp đầu tiên sau khi game over hay không. Nếu là đầu tiên, hàm show_gameover_screen() sẽ được gọi để hiển thị màn hình game over. Sau đó, biến first_round được đặt thành False để đảm bảo rằng màn hình game over chỉ hiển thị một lần.
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3 # Số mạng của người chơi được đặt lại thành 3 mạng
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png') #Hàm này được gọi để vẽ số mạng của người chơi lên màn hình, sử dụng hình ảnh mạng đỏ từ đường dẫn 'images/red_lives.png'.
        score = 0 #Điểm số của người chơi được đặt lại về 0.
    

    for event in pygame.event.get(): # vòng lập sử lí sự kiện 
        # checking for closing window
        if score > high_score:
            high_score = score  # Cập nhật điểm số cao nhất
        if event.type == pygame.QUIT: #Duyệt qua tất cả sự kiện Pygame và kiểm tra nếu có sự kiện QUIT (đóng cửa sổ game) thì dừng vòng lặp chính.
            game_running = False

    gameDisplay.blit(background, (0, 0)) #Dòng này vẽ nền của trò chơi lên màn hình,Hình nền này được vẽ từ góc (0, 0) của màn hình
    gameDisplay.blit(score_text, (0, 0))#Dòng này vẽ điểm số của người chơi lên màn hình. score_text là một đối tượng Surface của Pygame chứa thông tin về điểm số, được tạo ra từ hàm font.render(). Đối tượng này được vẽ từ góc (0, 0) của màn hình.
    font = pygame.font.Font(None, 36)
    text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
    gameDisplay.blit(text, (0, 20))
    pygame.display.update()
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')#Hàm này được gọi để vẽ số mạng của người chơi lên màn hình. 
                                                  #690 tọa độ x , 5 là tọa độ y của số mạng , player_lives số mạng của người chơi, còn kia là đường dẫn
    for key, value in data.items():#duyệt qua từng phần tử trong dictionary data, trong đó key là tên của quả cầu và value là thông tin về quả cầu đó.
        if value['throw']: # (value['throw'] == True), thực hiện các bước sau để di chuyển chúng:
            value['x'] += value['speed_x']          #: Di chuyển quả theo hướng x dựa trên tốc độ x.
            value['y'] += value['speed_y']          #lệnh gán  Di chuyển quả cầu theo hướng y dựa trên tốc độ y.
            value['speed_y'] += (1 * value['t'])    #Tăng tốc độ y để mô phỏng trọng lực.
            value['t'] += 1                         #Tăng giá trị t để sử dụng trong vòng lặp tiếp theo.
        

#Hiển Thị Quả Cầu trên Màn Hình:
            if value['y'] <= 800: #Nếu quả cầu không rơi ra khỏi màn hình (value['y'] <= 800), hiển thị quả cầu tại vị trí mới.
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #hiển thị trái cây bên trong màn hình một cách linh hoạt
            else:
                generate_random_viruss(key) #Nếu quả cầu rơi ra khỏi màn hình, hàm generate_random_viruss(key) được gọi để tạo lại một quả cầu mới.

            current_position = pygame.mouse.get_pos()   #Hàm này trả về tọa độ hiện tại của chuột trong hệ tọa độ pixel.()

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60: #Kiểm tra xem chuột có nằm trong phạm vi của quả hay không. Điều kiện này được kiểm tra để đảm bảo rằng quả chưa được bắn trúng (not value['hit']) và chuột nằm trong hình chữ nhật giới hạn của quả cầu (chiều rộng là 60 và chiều cao là 60).
                if key == 'bomb': # xử lí khi va cham với bom Nếu va chạm xảy ra với bom, giảm số mạng của người chơi (player_lives) và kiểm tra xem người chơi còn mạng không.
                    player_lives -= 1
                
                    if player_lives == 0:#Nếu người chơi hết mạng, ẩn đi hình ảnh các mạng và hiển thị màn hình game over.
#Nếu va chạm xảy ra với quả cầu bình thường, xử lý các thao tác liên quan, như tải hình ảnh phân nửa của quả cầu và tăng điểm (score).
                          
                        hide_cross_lives(690, 15) #được gọi để ẩn hình ảnh mạng ở tọa độ (690, 15).
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15) #khi mất mạng ẩn hình ảnh ở tọa độ (725,15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15) #khi mất mạng ẩn hình ảnh ở toaj độ (760;15)
                     
                    if player_lives < 0 :#Nếu số mạng của người chơi dưới 0 (player_lives < 0), tức là họ đã nhấp vào bom đủ số lần, màn hình game over được hiển thị bằng cách gọi hàm show_gameover_screen() và biến game_over được đặt thành True. Điều này thông báo rằng trò chơi đã kết thúc và cần phải reset.
                        show_gameover_screen()
                        game_over = True

                    half_virus_path = "images/explosion.png" #half_virus_path được đặt thành đường dẫn của hình ảnh một nửa của quả cầu hoặc hình ảnh bom nổ tùy thuộc vào việc va chạm với bom hay không.
                else:
                    half_virus_path = "images/" + "half_" + key + ".png"
                    if key == 'increase':
                        value['speed_x'] += increased_speed
                        value['speed_y'] += increased_speed
                    elif key == 'decrease':
                        value['speed_x'] += decreased_speed
                        value['speed_y'] += decreased_speed


                value['img'] = pygame.image.load(half_virus_path) #òng mã xử lý liên quan đến việc tải hình ảnh mới cho quả cầu
                value['speed_x'] += 10 #và tăng tốc độ x nếu quả đó không phải là boom 
                if key != 'bomb' : # nếu quả đó khác bom thì điểm số được tăng lên.
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255)) # Tạo lại đối tượng điểm văn bản hiển thị điểm số trên màn hình.
                value['hit'] = True # Đánh dấu quả cầu đã được bắn trúng để tránh xử lý trùng lặp.
        else:
            generate_random_viruss(key) #: Nếu quả cầu không được bắn trúng, tạo lại một quả cầu mới bằng cách gọi hàm generate_random_viruss(key)
    
    pygame.display.update()
    clock.tick(FPS)      # Cập nhật giao diện hiển thị trên màn hình và điều chỉnh tốc độ khung hình của trò chơi.  
pygame.quit() # kết thúc chương trình