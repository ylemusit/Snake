import pygame
from constants import WIDTH, HEIGHT, BLACK
from src.utils.records import read_records, write_records

font = pygame.font.SysFont("consolas", 24)
small = pygame.font.SysFont("consolas", 18)

class GameOver:
    def __init__(self, score):
        self.score = score
        self.name = ""
        self.records = read_records()
        self.new_record = not self.records or score > min(self.records)

    def handle_event(self, event):
        if self.new_record and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name:
                records = self.records + [self.score]
                write_records(sorted(records, reverse=True)[:5])
                return "menu"
            elif event.key == pygame.K_BACKSPACE and self.name:
                self.name = self.name[:-1]
            elif len(self.name) < 5 and event.unicode.isalnum():
                self.name += event.unicode.upper()
        elif not self.new_record and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        return None

    def draw(self, surface):
        surface.fill(BLACK)
        over = font.render("GAME OVER", True, (255, 255, 255))
        surface.blit(over, over.get_rect(center=(WIDTH // 2, 100)))

        score_surf = font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        surface.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, 150)))

        if self.new_record:
            prompt = small.render("Nuevo récord! Nombre (5 letras):", True, (255, 255, 0))
            surface.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 200)))
            name_surf = font.render(self.name + "_", True, (255, 255, 255))
            surface.blit(name_surf, name_surf.get_rect(center=(WIDTH // 2, 240)))
        else:
            esc = small.render("ESC para volver al menú", True, (255, 255, 255))
            surface.blit(esc, esc.get_rect(center=(WIDTH // 2, 200)))