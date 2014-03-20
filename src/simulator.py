"""Simulator Manager.

Usage:
  simulator SERVER (ins|pgw|ntf|sm|ldapp|smp|adcom) (install|uninstall)
  simulator SERVER upgrade (nds|pgw|ntf|check|ins|adm|sm) (install|uninstall)
  simulator SERVER pgw status (running|stopped|dead)
  simulator SERVER pgw limanagement (true|false)
  simulator SERVER pgw instances NUMBER
  simulator SERVER ntf status (running|stopped|dead)
  simulator SERVER sm status (master|slave|stopped|unknown|indeterminate)
  simulator SERVER ss (install|uninstall) ACTIVEADM
  simulator SERVER ss (start|stop)
  simulator SERVER smp (start|stop)
  simulator SERVER smp config DSADATA
  simulator SERVER adcom (status|stop|timeout) NUMBER
  simulator SERVER upgrade (nds|pgw|ntf) ostype (v80|v90)
  simulator SERVER check COMMAND EXITCODE [OUTPUT]
  simulator (-h | --help)
  simulator --version

Arguments:
  SERVER       hostname of the server
  ACTIVEADM    hostname of active ADM
  DSADATA      coma separated list of DSA id > 1,2,6
  NUMBER       plain integer
  COMMAND      upgradeBackup, upgradeBackupSize, upgradeHealthCheck_80, upgradeHealthCheck_90, upgradeRestore_80, upgradeRestore_90
  EXITCODE     0 - 255 (integer), 0 - success
  OUTPUT       result of the command
  
Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Simulator Manager 0.2')
    print(arguments)