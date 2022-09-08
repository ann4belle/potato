from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn
try:
    from msvcrt import getch
except ImportError:
    from getch import getch
import random

destiny = 0
destiny_task = None
potatoes = 0
potatoes_task = None
orcs = 0
orcs_task = None
orcs_removal_cost = 1
console = Console()

rprint('[bold]Welcome to Potato![/bold]\nOriginal game definition: https://twitter.com/deathbybadger/status/1567425842526945280\n' +
    'Implemented in Python by https://github.com/ann4belle\n\n[bold]Press any key to continue.[/bold]')
getch()
console.clear()
print('The premise is simple: you are a halfling, just trying to exist. Meanwhile, the dark lord rampages across the world. You do not care about this.' +
    ' You are trying to farm potatoes - because what could a halfling possibly do about it, anyway?')
print('Each turn, you roll to determine what event (if any) happens, which will effect one or more of your scores (Destiny, Potatoes, and Orc). Once one of your scores reaches 10, the game ends.')
print('You may spend one Potato to remove one Orc. This cost may increase as the game goes on.')
rprint('[bold]Press any key to start the game![/bold]')
getch()

while True:
    console.clear()
    with Progress(
        TextColumn('[progress.description]{task.description}'),
        BarColumn(),
        TextColumn('[progress.description]{task.completed}')
        ) as progress:
        destiny = 0
        potatoes = 0
        orcs = 0
        orc_removal_cost = 1
        destiny_task = progress.add_task('Destiny', total=10)
        potatoes_task = progress.add_task('Potatoes', total=10)
        orcs_task = progress.add_task('Orcs', total=10)
        while destiny < 10 and potatoes < 10 and orcs < 10:
            rprint('[bold]Press any key to roll.[/bold]')
            getch()
            match random.randrange(1, 4):
                case 1:
                    print('In the garden...')
                    match random.randrange(1, 7):
                        case 1:
                            rprint('You happily root about all day in your garden. [bold]+1 Potato[/bold]')
                            progress.advance(potatoes_task, 1)
                            potatoes += 1
                        case 2:
                            rprint('You narrowly avoid a visitor by hiding in a potato sack. [bold]+1 Potato[/bold], [bold]+1 Destiny[/bold]')
                            progress.advance(potatoes_task, 1)
                            progress.advance(destiny_task, 1)
                            potatoes += 1
                            destiny += 1
                        case 3:
                            rprint('A hooded stranger lingers outside your farm. [bold]+1 Destiny[/bold], [bold]+1 Orc[/bold]')
                            progress.advance(destiny_task, 1)
                            progress.advance(orcs_task, 1)
                            destiny += 1
                            orcs += 1
                        case 4:
                            if potatoes > 0:
                                rprint('Your field is ravaged in the night by unseen enemies. [bold]+1 Orc[/bold], [bold]-1 Potato[/bold]')
                                progress.advance(potatoes_task, -1)
                                potatoes -= 1
                            else:
                                rprint('Your field is ravaged in the night by unseen enemies. [bold]+1 Orc[/bold]')
                            progress.advance(orcs_task, 1)
                            orcs += 1
                        case 5 if potatoes > 0:
                            rprint('You trade potatoes for other delicious foodstuffs. [bold]-1 Potato[/bold]')
                            progress.advance(potatoes_task, -1)
                            potatoes -= 1
                        case 5 if potatoes == 0:
                            rprint('You try trade potatoes for other delicious foodstuffs, but then you remember you don\'t have any potatoes. This makes you sad.')
                        case 6:
                            rprint('You burrow into a bumper crop of potatoes. Do you cry with joy? Possibly. [bold]+2 Potatoes[/bold]')
                            progress.advance(potatoes_task, 2)
                            potatoes += 2
                case 2:
                    print('A knock at the door...')
                    match random.randrange(1, 7):
                        case 1:
                            rprint('A distant cousin. They are after your potatoes. They may snitch on you. [bold]+1 Orc[/bold]')
                            progress.advance(orcs_task, 1)
                            orcs += 1
                        case 2:
                            rprint('A dwarven stranger. You refuse them entry. Ghastly creatures. [bold]+1 Destiny[/bold]')
                            progress.advance(destiny_task, 1)
                            destiny += 1
                        case 3:
                            rprint('A wizard strolls by. You pointedly draw the curtains. [bold]+1 Orc[/bold], [bold]+1 Destiny[/bold]')
                            progress.advance(orcs_task, 1)
                            progress.advance(destiny_task, 1)
                            orcs += 1
                            destiny += 1
                        case 4:
                            if potatoes > 0:
                                rprint('There are rumors of war in the reaches. You eat some potatoes. [bold]-1 Potato[/bold], [bold]+2 Orcs[/bold]')
                                progress.advance(potatoes_task, -1)
                                potatoes -= 1
                            else:
                                rprint('There are rumors of war in the reaches. You go to eat some potatoes, but remember you don\'t have any. This makes you sad. [bold]+2 Orcs[/bold]')
                            progress.advance(orcs_task, 2)
                            orcs += 2
                        case 5:
                            rprint('It\'s an elf. They are not serious people. [bold]+1 Destiny[/bold]')
                            progress.advance(destiny_task, 1)
                            destiny += 1
                        case 6:
                            rprint('It\'s a sack of potatoes from a generous neighbor. You really must remember to pay them a visit one of these years. [bold]+2 Potatoes[/bold]')
                            progress.advance(potatoes_task, 2)
                            potatoes += 2
                case 3 if orc_removal_cost < 9:
                    orc_removal_cost += 1
                    print('The world becomes a darker, more dangerous place. From now on, removing an Orc costs an additional Potato (this is cumulative). Current cost: ' + str(orc_removal_cost))
                case 3 if orc_removal_cost == 9:
                    print('Nothing notable happens today.')
            if potatoes >= orc_removal_cost and orcs > 0:
                print('You can scare away an orc. This will cost ' + ('1 potato.' if orc_removal_cost == 1 else (str(orc_removal_cost) + ' potatoes.')) + ' Do so? (y/n)')
                answer = None
                while answer != 'y' and answer != 'n':
                    answer = getch().lower()
                    try:
                        answer = answer.decode()
                    except: AttributeError
                    if answer == 'n':
                        pass
                    elif answer != 'y':
                        print('You need to answer properly. Remove an orc? (y/n)')
                if answer == 'y':
                    rprint('You hurl ' + ('a potato ' if orc_removal_cost == 1 else 'some potatoes ')
                     + 'to scare an orc away. [bold]-' + str(orc_removal_cost) + (' Potato[/bold]' if orc_removal_cost == 1 else ' Potatoes[/bold]') + ', [bold]-1 Orc[/bold]')
                    progress.advance(potatoes_task, -orc_removal_cost)
                    progress.advance(orcs_task, -1)
                    potatoes -= orc_removal_cost
                    orcs -= 1
    if potatoes >= 10:
        rprint('[bold]You have ten sacks of potatoes![/bold]\nYou have enough potatoes that you can go underground and not return to the surface until the danger is past. \
        You nestle down into your burrow and enjoy your well-earned rest.')
    elif orcs >= 10:
        rprint('[bold]Orcs found your potato farm![/bold] Alas, orcs are not nearly as interested in potatoes as they are in eating you, and you end up in a cookpot.')
    elif destiny >= 10:
        rprint('[bold]Your destiny awaits![/bold]\nAn interfering bard or wizard turns up at your doorstep with a quest, and you are whisked away against your will on an adventure.')
    answer = None
    print('Play again? (y/n)')
    while answer != 'y' and answer != 'n':
        answer = input().lower()
        if answer == 'n':
            exit()
        elif answer != 'y':
            print('You need to answer properly. Play again? (y/n)')
