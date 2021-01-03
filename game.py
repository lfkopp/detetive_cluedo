#%%
import random

with open('similation.txt','w+') as f:
    for n in range(5000):
        num_players = 3
        #%%
        suspects = {'verde','vermelho','azul','amarelo','rosa','preto','branco'}
        weapons = {'faca','veneno','corda','pistola','pé de cabra','bomba atômica'}
        rooms = {'restaurante','boate','biblioteca','escola','prefeitura','cinema','cemitério','mansão'}

        #%%
        solution = {  'suspect': random.choice(tuple(suspects)),
                    'weapon' : random.choice(tuple(weapons)),
                    'room'   : random.choice(tuple(rooms))}
        #print('solution:',solution)

        #%%

        all_cards = list(set(suspects | weapons | rooms) - set(solution.values()))
        random.shuffle(all_cards)    


        #print('all_cards:',len(all_cards),all_cards)
        # %%
        class Player:
            def __init__(self, name):
                self.guess = {  'suspect': suspects,
                                'weapon' : weapons,
                                'room'   : rooms}
                self.hand = set()
                self.name = name
            def remove_guess(self, card):
                self.card = card
                self.guess['suspect']  = self.guess['suspect'] - {self.card}
                self.guess['weapon'] = self.guess['weapon'] - {self.card}
                self.guess['room'] = self.guess['room'] - {self.card}
            def add_hand(self, card):
                self.card = card
                self.hand = self.hand | {self.card}
                self.remove_guess(card)
            def make_guess(self):
                return {  'suspect': random.choice(tuple(self.guess['suspect'])),
                    'weapon' : random.choice(tuple(self.guess['weapon'])),
                    'room'   : random.choice(tuple(self.guess['room']))}
            def answer_guess(self, guess_1):
                return [guess_1[v] for v in guess_1 if guess_1[v] in self.hand]

        # %%
        players = {}
        names = ['Margarida','Pato Donald', 'Tio Patinhas', 'Mickey', 'Minnie','Pateta', 'Pluto', 'Hortênsia']
        random.shuffle(names)
        for i in range(num_players):
            name = names.pop()
            players[name] = Player(name)
        # %%
        deck = list(all_cards)
        while(len(deck) >= num_players):
            for p in players:
                players[p].add_hand(deck.pop())
        print('excluded cards:',deck)
        for c in deck:
            for p in players:
                players[p].remove_guess(c)

        # %%
        # print("hands")
        # for p in players:
        #     print(players[p].name,players[p].hand)


        # print("guesses")
        # for p in players:
        #     print(players[p].name,players[p].guess)
        #%%
        def play(player):
            hint = players[player].make_guess()
            #print('hint from',player,hint)
            if solution == hint:
                print(player," won the game!!")
                return True
            else:
                ps = list(players.keys())
                i = ps.index(player)
                suspect = ps[i+1:]+ps[:i]
                for j in suspect:
                    answer = players[j].answer_guess(hint)
                    #print(j,'answer:',answer)
                    if answer:
                        players[player].remove_guess(answer[0])
                        return False
                
        # %%

        has_winner = False
        ps = list(players.keys())
        count = 0
        while not has_winner:
            has_winner = play(ps[count % num_players])
            count += 1
        f.write(str(count)+'\n')
        # %%
