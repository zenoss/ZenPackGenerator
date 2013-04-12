import os
def CreateZenPackStructure(zpId,destroot='/opt/zenoss/ZenPacks'):

    parts = zpId.split('.')
    if not os.path.exists(destroot):
        os.mkdir(destroot,0750)

    destdir = os.path.join(destroot,zpId)


if __name__ == '__main__':
    try:
        zp = ZenPackCmd()
        zp.run()
    except ZenPackException, e:
        sys.stderr.write('%s\n' % str(e))
        sys.exit(-1)
