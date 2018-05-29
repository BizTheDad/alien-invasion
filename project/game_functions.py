import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_events(settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(settings, screen, ship, aliens, bullets):
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    pygame.display.flip()


def update_bullets(aliens, bullets):
    bullets.update()

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def create_fleet(settings, screen, ship, aliens):
    alien_width, alien_height = get_alien_height_width(settings, screen)
    number_aliens_x = get_number_aliens(settings, alien_width)
    number_rows = get_number_rows(settings, ship.rect.height, alien_height)

    for row in range(number_rows):
        for alien_number in range(number_aliens_x):
            aliens.add(create_alien(settings, screen, alien_number, row))


def get_alien_height_width(settings, screen):
    alien = Alien(settings, screen)
    return alien.rect.width, alien.rect.height


def get_number_aliens(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def create_alien(settings, screen, alien_number, row_number):
    alien = Alien(settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    return alien


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y / (2 * alien_height))


def update_aliens(settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed

    settings.fleet_direction *= -1


def ship_hit(settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break
