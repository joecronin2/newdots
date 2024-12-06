from yeelight import Bulb



light1 = Bulb("10.79.60.104")
light2 = Bulb("10.79.60.142")
light3 = Bulb("10.79.60.103")

bulbs = [light1, light2, light3]

for bulb in bulbs:
    bulb.toggle()
