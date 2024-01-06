#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    info('Nhap vao dia chi co dang a.b.c.0/24\n')
    a = input('Nhap vao a =')
    b = input('Nhap vao b =')
    c = input('Nhap vao c =')
    info('Mang sau khi nhap {0}.{1}.{2}.0/24\n'.format(a,b,c))
    net = Mininet( topo=None,
                   build=False,
                   ipBase='{0}.{1}.{2}.0/24'.format(a,b,c))

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r2 = net.addHost('r2', cls=Node, ip='{0}.{1}.{2}.65'.format(a,b,c))
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='{0}.{1}.{2}.129'.format(a,b,c))
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1 = net.addHost('r1', cls=Node, ip='{0}.{1}.{2}.1'.format(a,b,c))
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='{0}.{1}.{2}.66'.format(a,b,c), defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='{0}.{1}.{2}.2'.format(a,b,c), defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='{0}.{1}.{2}.130'.format(a,b,c), defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, r1)
    net.addLink(h2, r2)
    net.addLink(h3, r3)
    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(r1, r3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')
    h1.cmd('ifconfig h1-eth0 {0}.{1}.{2}.2/26 up'.format(a,b,c))
    h2.cmd('ifconfig h2-eth0 {0}.{1}.{2}.66/26 up'.format(a,b,c))
    h3.cmd('ifconfig h3-eth0 {0}.{1}.{2}.130/26 up'.format(a,b,c))
    r1.cmd('ifconfig r1-eth0 {0}.{1}.{2}.1/26 up'.format(a,b,c))
    r1.cmd('ifconfig r1-eth1 {0}.{1}.{2}.193/30 up'.format(a,b,c))
    r1.cmd('ifconfig r1-eth2 {0}.{1}.{2}.201/30 up'.format(a,b,c))
    r2.cmd('ifconfig r2-eth0 {0}.{1}.{2}.65/26 up'.format(a,b,c))
    r2.cmd('ifconfig r2-eth1 {0}.{1}.{2}.194/30 up'.format(a,b,c))
    r2.cmd('ifconfig r2-eth2 {0}.{1}.{2}.197/30 up'.format(a,b,c))
    r3.cmd('ifconfig r3-eth0 {0}.{1}.{2}.129/26 up'.format(a,b,c))
    r3.cmd('ifconfig r3-eth1 {0}.{1}.{2}.198/30 up'.format(a,b,c))
    r3.cmd('ifconfig r3-eth2 {0}.{1}.{2}.202/30 up'.format(a,b,c))
    h1.cmd('route add default gw {0}.{1}.{2}.1'.format(a,b,c))
    h2.cmd('route add default gw {0}.{1}.{2}.65'.format(a,b,c))
    h3.cmd('route add default gw {0}.{1}.{2}.129'.format(a,b,c))
    r1.cmd('route add -net {0}.{1}.{2}.64/26 gw {0}.{1}.{2}.194'.format(a,b,c))
    r1.cmd('route add -net {0}.{1}.{2}.128/26 gw {0}.{1}.{2}.202'.format(a,b,c))
    r2.cmd('route add -net {0}.{1}.{2}.0/26 gw {0}.{1}.{2}.193'.format(a,b,c))
    r2.cmd('route add -net {0}.{1}.{2}.128/26 gw {0}.{1}.{2}.198'.format(a,b,c))
    r3.cmd('route add -net {0}.{1}.{2}.0/26 gw {0}.{1}.{2}.201'.format(a,b,c))
    r3.cmd('route add -net {0}.{1}.{2}.64/26 gw {0}.{1}.{2}.197'.format(a,b,c))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

