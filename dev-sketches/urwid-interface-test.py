import urwid

def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    txt.set_text(repr(key))

a=[1,2,3,4,5,6,7,1]
b=['I','II','III','IV','V','VI','VII','I']

header = urwid.Text(u"birdears", align="center")
footer = urwid.Text(u"https://github.com/iacchus/birdears", align="center")

clm = urwid.Columns([urwid.Text(str(n), align='center') for n in a])
clm2 = urwid.Columns([urwid.Text(n, align='center') for n in b])
pile1 = urwid.Pile([clm, clm2])
lbox = urwid.LineBox(pile1)
fill = urwid.Filler(lbox, valign='middle', min_height=3)
padd = urwid.Padding(fill, align='center', width=('relative',40))

frame = urwid.Frame(padd, header=header, footer=footer)

loop = urwid.MainLoop(frame, unhandled_input=show_or_exit)
loop.run()
