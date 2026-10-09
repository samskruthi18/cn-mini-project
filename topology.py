from mininet.topo import Topo


class ReservationTopology(Topo):
    def build(self):
        # Create three virtual computers
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')

        # Create one OpenFlow-capable switch
        s1 = self.addSwitch('s1', protocols='OpenFlow13')

        # Connect every computer to the switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)


topos = {'reservation': lambda: ReservationTopology()}
