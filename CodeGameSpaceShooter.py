import pygame  # Mengimpor modul Pygame untuk membuat game
import random  # Mengimpor modul random untuk menghasilkan angka acak
import time  # Mengimpor modul time untuk mengelola waktu
import sys  # Mengimpor modul sys untuk mengelola parameter sistem

# Pengaturan layar
SCREEN_WIDTH = 800  # Lebar layar game
SCREEN_HEIGHT = 600  # Tinggi layar game
WHITE = (255, 255, 255)  # Warna putih untuk teks dan elemen lainnya
BLACK = (0, 0, 0)  # Warna hitam untuk latar belakang dan elemen lainnya
GRAY = (200, 200, 200)  # Warna abu-abu untuk elemen lainnya
DARK_GRAY = (100, 100, 100)  # Warna abu-abu gelap untuk tombol hover

pygame.init()  # Inisialisasi Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Membuat jendela game dengan ukuran yang ditentukan
pygame.display.set_caption("Space Shooter")  # Menentukan judul jendela game

# Muat gambar
player_image = pygame.image.load(r"c:\Users\dwi wahyu utami\Downloads\roket 1.png")  # Memuat gambar pesawat pemain
enemy_image = pygame.image.load(r"c:\Users\dwi wahyu utami\Downloads\ufo 2.webp")  # Memuat gambar musuh
explosion_image = pygame.image.load(r"c:\Users\dwi wahyu utami\Downloads\ledakan.png")  # Memuat gambar ledakan
background_image = pygame.image.load(r"c:\Users\dwi wahyu utami\Downloads\yuhu.webp")  # Memuat gambar latar belakang
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Mengubah ukuran gambar latar belakang

# Atur transparansi warna hitam pada gambar
player_image.set_colorkey((0, 0, 0))  # Menyeting warna hitam menjadi transparan pada gambar pesawat pemain
enemy_image.set_colorkey((0, 0, 0))  # Menyeting warna hitam menjadi transparan pada gambar musuh
explosion_image.set_colorkey((0, 0, 0))  # Menyeting warna hitam menjadi transparan pada gambar ledakan

# Kelas Pemain (POLYMORPHISM)
class Player(pygame.sprite.Sprite):  # Mendefinisikan kelas Player sebagai sprite #ABSTRACTION
    def __init__(self):
        super().__init__()  # Memanggil konstruktor kelas induk (Sprite)
        self.image = pygame.transform.scale(player_image, (50, 100))  # Mengubah ukuran gambar pesawat pemain
        self.rect = self.image.get_rect()  # Mendapatkan objek rect dari gambar pesawat pemain
        self.rect.centerx = 400  # Menentukan posisi horizontal tengah pesawat pemain
        self.rect.bottom = 590  # Menentukan posisi vertikal bawah pesawat pemain
        self.speed_x = 0  # Kecepatan horizontal pesawat pemain
        self.health = 100  # Kesehatan pesawat pemain

    def update(self):
        self.rect.x += self.speed_x  # Memperbarui posisi horizontal pesawat berdasarkan kecepatan
        if self.rect.left < 0:  # Membatasi pesawat agar tidak keluar dari layar kiri
            self.rect.left = 0
        if self.rect.right > 800:  # Membatasi pesawat agar tidak keluar dari layar kanan
            self.rect.right = 800

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  # Membuat objek peluru baru dari posisi pesawat
        return bullet

# Kelas Musuh (POLYMORPHISME)
class Enemy(pygame.sprite.Sprite):  # Mendefinisikan kelas Musuh sebagai sprite (ABSTRACTION)
    def __init__(self):
        super().__init__()  #INHERITANCE # Memanggil konstruktor kelas induk (Sprite)
        self.image = pygame.transform.scale(enemy_image, (50, 50))  # Mengubah ukuran gambar musuh
        self.rect = self.image.get_rect()  # Mendapatkan objek rect dari gambar musuh
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)  # Menentukan posisi horizontal musuh secara acak
        self.rect.y = random.randrange(-100, -40)  # Menentukan posisi vertikal musuh secara acak di luar layar
        self.speed_y = random.randrange(2, 6)  # Menentukan kecepatan vertikal musuh secara acak

    def update(self):
        self.rect.y += self.speed_y  # Memperbarui posisi vertikal musuh
        if self.rect.top > SCREEN_HEIGHT:  # Jika musuh melewati batas layar, posisinya direset
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(2, 6)  # Menentukan kecepatan vertikal baru secara acak

# Kelas Peluru
class Bullet(pygame.sprite.Sprite):  # Mendefinisikan kelas Bullet sebagai sprite
    def __init__(self, x, y): # INHERITANCE
        super().__init__()  # Memanggil konstruktor kelas induk (Sprite)
        self.image = pygame.Surface((5, 20))  # Membuat permukaan baru untuk peluru
        self.image.fill((255, 0, 0))  # Mengisi peluru dengan warna putih
        self.rect = self.image.get_rect()  # Mendapatkan objek rect dari peluru
        self.rect.centerx = x  # Menentukan posisi horizontal peluru
        self.rect.bottom = y  # Menentukan posisi vertikal peluru
        self.speed_y = -10  # Kecepatan peluru ke atas

    def update(self):
        self.rect.y += self.speed_y  # Memperbarui posisi vertikal peluru
        if self.rect.bottom < 0:  # Jika peluru melewati batas layar, peluru dihapus
            self.kill()

# Kelas Ledakan
class Explosion(pygame.sprite.Sprite):  # Mendefinisikan kelas Ledakan sebagai sprite
    def __init__(self, x, y):
        super().__init__()  # Memanggil konstruktor kelas induk (Sprite)
        self.image = pygame.transform.scale(explosion_image, (50, 50))  # Mengubah ukuran gambar ledakan
        self.rect = self.image.get_rect()  # Mendapatkan objek rect dari gambar ledakan
        self.rect.center = (x, y)  # Menentukan posisi ledakan
        self.life_time = 20  # Waktu hidup ledakan

    def update(self):
        self.life_time -= 1  # Mengurangi waktu hidup ledakan
        if self.life_time <= 0:  # Jika waktu hidup habis, ledakan dihapus
            self.kill()

# Fungsi menggambar teks
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)  # Membuat objek font dengan ukuran yang ditentukan
    text_surface = font.render(text, True, WHITE)  # Menggambar teks dengan warna putih
    text_rect = text_surface.get_rect(center=(x, y))  # Mendapatkan posisi teks
    surface.blit(text_surface, text_rect)  # Menampilkan teks pada permukaan

# Fungsi game loop
def game_loop(screen, background_image):
    all_sprites = pygame.sprite.Group()  # Grup untuk semua sprite
    enemies = pygame.sprite.Group()  # Grup untuk musuh
    bullets = pygame.sprite.Group()  # Grup untuk peluru
    explosions = pygame.sprite.Group()  # Grup untuk ledakan

    player = Player()  # Membuat objek pemain
    all_sprites.add(player)  # Menambahkan pemain ke grup sprite

    for _ in range(8):  # Membuat 8 musuh
        enemy = Enemy()  # Membuat objek musuh
        all_sprites.add(enemy)  # Menambahkan musuh ke grup sprite
        enemies.add(enemy)  # Menambahkan musuh ke grup musuh

    score = 0  # Skor permainan
    start_time = time.time()  # Waktu mulai permainan
    clock = pygame.time.Clock()  # Mengatur kecepatan frame game
    running = True  # Status permainan

    while running:
        clock.tick(60)  # Mengatur FPS game ke 60
        for event in pygame.event.get():  # Mengambil event dari input pengguna
            if event.type == pygame.QUIT:  # Jika pemain menutup jendela, keluar dari game
                return score
            if event.type == pygame.KEYDOWN:  # Jika tombol ditekan
                if event.key == pygame.K_LEFT:  # Jika tombol kiri ditekan
                    player.speed_x = -5  # Gerakkan pemain ke kiri
                if event.key == pygame.K_RIGHT:  # Jika tombol kanan ditekan
                    player.speed_x = 5  # Gerakkan pemain ke kanan
                if event.key == pygame.K_SPACE:  # Jika tombol spasi ditekan
                    bullet = player.shoot()  # Membuat peluru baru
                    all_sprites.add(bullet)  # Menambahkan peluru ke grup sprite
                    bullets.add(bullet)  # Menambahkan peluru ke grup peluru
            if event.type == pygame.KEYUP:  # Jika tombol dilepas
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:  # Jika tombol kiri atau kanan dilepas
                    player.speed_x = 0  # Hentikan pergerakan horizontal pemain

        all_sprites.update()  # Memperbarui semua sprite

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)  # Mengecek tumbukan antara musuh dan peluru
        for hit in hits:
            score += 10  # Tambah skor
            enemy = Enemy()  # Membuat musuh baru
            all_sprites.add(enemy)  # Menambahkan musuh baru ke grup sprite
            enemies.add(enemy)  # Menambahkan musuh baru ke grup musuh
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)  # Membuat ledakan
            all_sprites.add(explosion)  # Menambahkan ledakan ke grup sprite
            explosions.add(explosion)  # Menambahkan ledakan ke grup ledakan

        hits = pygame.sprite.spritecollide(player, enemies, True)  # Mengecek tumbukan antara pemain dan musuh
        for hit in hits:
            player.health -= 10  # Mengurangi kesehatan pemain
            enemy = Enemy()  # Membuat musuh baru
            all_sprites.add(enemy)  # Menambahkan musuh baru ke grup sprite
            enemies.add(enemy)  # Menambahkan musuh baru ke grup musuh
            if player.health <= 0:  # Jika kesehatan pemain habis
                running = False  # Mengakhiri permainan

        current_time = time.time()  # Mengambil waktu saat ini
        screen.blit(background_image, (0, 0))  # Menampilkan latar belakang
        all_sprites.draw(screen)  # Menampilkan semua sprite
        draw_text(screen, f"Score: {score}", 36, 70, 30)  # Menampilkan skor
        draw_text(screen, f"Health: {player.health}", 36, 70, 70)  # Menampilkan kesehatan pemain
        draw_text(screen, f"Time: {int(current_time - start_time)} s", 36, 70, 110)  # Menampilkan waktu

        pygame.display.flip()  # Memperbarui tampilan layar

    return score  # Mengembalikan skor akhir

# Kelas Button
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)  # Membuat objek rect untuk tombol
        self.text = text  # Teks yang ditampilkan pada tombol
        self.color = color  # Warna tombol
        self.hover_color = hover_color  # Warna tombol saat di-hover
        self.current_color = color  # Menyimpan warna tombol saat ini

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)  # Menggambar tombol dengan warna saat ini
        pygame.draw.rect(surface, WHITE, self.rect, 3)  # Menggambar garis tepi tombol
        font = pygame.font.Font(None, 50)  # Membuat objek font dengan ukuran 50
        text_surface = font.render(self.text, True, WHITE)  # Menggambar teks pada tombol
        text_rect = text_surface.get_rect(center=self.rect.center)  # Menentukan posisi teks pada tombol
        surface.blit(text_surface, text_rect)  # Menampilkan teks pada tombol

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:  # Jika mouse bergerak
            self.current_color = self.hover_color if self.rect.collidepoint(event.pos) else self.color  # Menentukan warna tombol saat di-hover

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)  # Mengecek apakah tombol diklik

# Fungsi menu utama
def main_menu():
    start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 70, "Start", BLACK, DARK_GRAY)  # Membuat tombol start
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 70, "Quit", BLACK, DARK_GRAY)  # Membuat tombol quit

    while True:
        for event in pygame.event.get():  # Mengambil event dari input pengguna
            if event.type == pygame.QUIT:  # Jika pemain menutup jendela, keluar dari menu
                return False
            start_button.handle_event(event)  # Menangani event untuk tombol start
            quit_button.handle_event(event)  # Menangani event untuk tombol quit
            if start_button.is_clicked(event):  # Jika tombol start diklik
                return True
            if quit_button.is_clicked(event):  # Jika tombol quit diklik
                return False

        screen.fill(BLACK)  # Mengisi latar belakang dengan warna hitam
        draw_text(screen, "Space Shooter", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)  # Menampilkan judul game
        start_button.draw(screen)  # Menampilkan tombol start
        quit_button.draw(screen)  # Menampilkan tombol quit
        pygame.display.flip()  # Memperbarui tampilan layar

# Fungsi game over
def show_game_over(final_score):
    replay_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 70, "Replay", BLACK, DARK_GRAY)  # Membuat tombol replay
    quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 70, "Quit", BLACK, DARK_GRAY)  # Membuat tombol quit

    while True:
        for event in pygame.event.get():  # Mengambil event dari input pengguna
            if event.type == pygame.QUIT:  # Jika pemain menutup jendela, keluar dari game over
                return False
            replay_button.handle_event(event)  # Menangani event untuk tombol replay
            quit_button.handle_event(event)  # Menangani event untuk tombol quit
            if replay_button.is_clicked(event):  # Jika tombol replay diklik
                return True
            if quit_button.is_clicked(event):  # Jika tombol quit diklik
                return False

        screen.fill(BLACK)  # Mengisi latar belakang dengan warna hitam
        draw_text(screen, "Game Over", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)  # Menampilkan teks game over
        draw_text(screen, f"Score: {final_score}", 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)  # Menampilkan skor akhir
        replay_button.draw(screen)  # Menampilkan tombol replay
        quit_button.draw(screen)  # Menampilkan tombol quit
        pygame.display.flip()  # Memperbarui tampilan layar

# Fungsi utama
def main():
    while True:
        if not main_menu():  # Menampilkan menu utama dan mengecek apakah permainan dimulai
            break
        final_score = game_loop(screen, background_image)  # Menjalankan game loop dan mendapatkan skor akhir
        if not show_game_over(final_score):  # Menampilkan game over dan mengecek apakah pemain ingin bermain lagi
            break
    pygame.quit()  # Menutup Pygame
    sys.exit()  # Keluar dari program

if __name__ == "__main__":  # Jika skrip dijalankan langsung
    main()  # Menjalankan fungsi utama
