from tkinter import *
from get_data import *
from get_teams_names import get_teams
root = Tk()
root.title('teams')

j = 0 
z = 0
i = 0
for x in get_teams():
    button_name = 'button_' + str(i)
    print(button_name)  
    i += 1
    if z < 7:
        driver = team(i)
        Button(root, text = x, padx = 100, command = data(), font=('arial',20)).grid(row=z, column=j)
        z += 1  
    else:
        j += 1
        z = 0
    
    print(i)  
root.mainloop()


# button_1 = Button(root, text = team_names[i], padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_2 = Button(root, text = 'bucks', padx = 100, command = lambda: Get_info.team(2) , font=('arial',20))
# button_3 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(3) , font=('arial',20))
# button_4 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(4) , font=('arial',20))
# button_5 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team() , font=('arial',20))
# button_6 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_7 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_8 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_9 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_10 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_11 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_12 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_13 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_14 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_15 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_16 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_17= Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_18 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_19 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_20 = Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_21= Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))
# button_22= Button(root, text = '76ers', padx = 100, command = lambda: Get_info.team(1) , font=('arial',20))


# button_1.grid(row=1)
# button_2.grid(row=2)
# button_3.grid(row=3)
# button_4.grid(row=4)
# button_5.grid(row=5)
# button_6.grid(row=6)
# button_7.grid(row=7)





'''
def scenariox():
    player1 = ''
    url1 = ''
    player2 = ''
    url2 = ''
    player3 = ''
    url3 = ''
    player4 = ''
    url4 = ''
    player5 = ''
    url5 = ''
    root1 = Tk() 
    root1.title('76ers')
    button_1 = Button(root1, text = player1, padx = 100, font=('arial',20),  command = lambda: get_csv(player1, url1))
    button_2 = Button(root1, text = player2, padx = 100, font=('arial',20),  command = lambda: get_csv(player2, url2))
    button_3 = Button(root1, text = player3, padx = 100, font=('arial',20),  command = lambda: get_csv(player3, url3))
    button_4 = Button(root1, text = player4, padx = 100, font=('arial',20),  command = lambda: get_csv(player4, url4))
    button_5 = Button(root1, text = player5, padx = 100, font=('arial',20),  command = lambda: get_csv(player5, url5))
    button_1.grid(row=1)
    button_2.grid(row=2)
    button_3.grid(row=3)
    button_4.grid(row=4)
    button_5.grid(row=5)
    root1.mainloop()
    '''
