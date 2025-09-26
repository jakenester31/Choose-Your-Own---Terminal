hell = {
    'start': ['Good morning!',['get up','5 more minutes'],['ready1','sleep1']],
    'ready1': ['You get ready for school, ready for monday, and gleefully walk to the bus station and wait.',['sit down','stand','jump in front of a truck'],['pre-bus sit','pre-bus stand','isekai']],
    'ready2': ['You are now late and so you rush, forgetting to put on your hair tie, you run to the bus station and wait',['sit down','stand','sleep'],['pre-bus sit','pre-bus stand','pre-bus sleep']],
    
    'sleep1':['You sleep for 5 more minutes, time to get up.',['get up','5 more minutes!'],['ready2','sleep2']],
    'sleep2': ['You sleep for another 5 minutes, you are going to be late.',['get up','5 MORE MINUTES!!!'],['ready2','sleep3']],
    'sleep3':'You never get up. You think 5 more minutes over and over. You have been in a comma for 10 years, and soon, many more.',
    
    'pre-bus stand': ['you stand and let an elderly lady with her grandchild sit. She thanked you and the child gave you a candy',['wait'],['bus arrival']],
    'pre-bus sit': ['You sit down and stare into the sunken eyes of an old lady, her grandchild is crying because his legs hurt. Asshole.',['wait'],['bus arrival']],
    'pre-bus sleep': 'You never wake up. You are now a ghost and as you stare down you notice a knife sticking out of your chest. Those damn racoons.',
    
    'bus arrival':['the bus arrives, and you get on, handing the driver some change as he lets go through. You sit in the back.',['signal car honk','listen to music','be social'],['bus honk','bus music','bus social']],
    'bus honk':'You signal to a truck for it honk and it honks. The bus driver was not expecting that and crashed the bus. You got a free week off from school, and a suspicion was the least of your worries. Blue and red lights are engraved in your memories.',
    'bus music':['You listen to music and feel the emotions drain out of you as they were replaced with pure mental silence',['continue'],['bus continue']],
    'bus social':['You try and talk to others but they scoff at you and then continue talking as if your not there. Apparently other think of you as the "weird kid"',['cry','hold it in','attack'],['bus social cry','bus social hold','bus social attack']],
    
    'isekai': ['The truck hit the breaks and veered into a young child, its all your fault',['mourn'],['isekai2']],
    'isekai2': 'You grab a knife from your lunch box and stab yourself repeatedly. You died, and you killed three people. Hell is waiting for you',
    
    'bus social cry':['Tears start to roll silently and even then no one cared. You sit down but not at the back, someone stole your seat.',['continue'],['bus continue']],
    'bus social hold':['You try and try to hold your tears in, none roll down your cheek but your eyes are now red. You sit down and listen to music',['continue'],['bus continue']],
    'bus social attack':['You lung at the kids, grab and rip their hair. But they overpower you and you are pushed to the ground. Stomped on repeatedly until the bus driver stops and kicks you out. You should thank him later',['ANGER'],['bus social attack result']],
    'bus social attack result': 'Anger fills every fiber of your being until other emotions start to take over. Sadness, confusion, hatred, you get the gist? You go home and become a hobbit, a hobbit crazy cat lady. Even now at age 30 you have not forgotten.',
    
    'bus continue': ['You wait and wait in silence until the bus stops and finally you get out. Your at your stupid, god forsaken school. Damn mondays.',['go to first period','go to the office',''],[]],
}

def run(obj,at):
    # initiate
    current = obj[at]
    if isinstance(current,str):
        print(current)
        return
    # body
    while True:
        while True:
            print()
            res = input(current[0] + ' ' + inputBuilder(current[1]) + ' >> ')
            if res in current[1]: break
        try:
            current = obj[current[2][current[1].index(res)]]
            if isinstance(current,str):
                print(current)
                break
        except KeyError:
            print(f'An Error occurred: "{res}" is an invalid reference')

def inputBuilder(val:list):
    string = '( '
    for i, item in enumerate(val):
        string += item
        if i != len(val) - 1: 
            string += ', '
    return string + ' )'

run(hell,'start')