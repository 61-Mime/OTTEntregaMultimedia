import sys
import ottNode
import atexit

bootstrapper = sys.argv

server = bootstrapper[1]

node = ottNode.OttNode([], server)

atexit.register(node.exitMessage)

node.initClient(server)
