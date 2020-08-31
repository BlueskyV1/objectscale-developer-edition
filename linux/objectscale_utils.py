import os
import subprocess

class objectscale_utility:
    helm_chart_url = "https://^@raw.githubusercontent.com/emcecs/charts/master/docs"
    objectscale_path: str
    is_valid_install: bool

    def __init__(self):
        self.objectscale_path = ''
        self.is_valid_install = False

    def check_objectscale_installation(self, PATH=os.getenv('PATH')) -> bool:
        print('Verifying Objectscale Installation.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('helm init', shell=True)
        result = subprocess.check_output('helm repo list', shell=True)
        result = result.decode(encoding='ascii').lower()
        if result.find('ecs-cluster') == -1:
            print('ECS-cluster not installed')
            return False
        if result.find('objectscale-manager') == -1:
            print('Objectscale not installed')
            return False
        print('All Objectscale components running, Install not necessary')
        return True


    def get_objectscale_version(self):
        print('Objectscale version.')
        self.start_minikube_if_stoppped()

    def clean_objectscale(self):
        print('Cleaning objectscale.')
        self.start_minikube_if_stoppped()
        print('Objectscale Cleaned.')

    def uninstall_objectscale(self):
        print('Uninstalling objectscale.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('helm list | "%CD%/lib_distr/gawk/awk.exe" "{print $1}"', shell=True)
        result = result.decode(encoding='ascii').lower()
        results = result.split('\n')
        for s in results:
            if not s.find('ecs-cluster') == -1:
                os.system('helm uninstall '+s)
            if not s.find('objs-mgr') == -1:
                os.system('helm uninstall '+s)

    def install_objectscale(self, token: str, PATH=os.getenv('PATH')):
        print('Installing Objectscale.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('helm repo list', shell=True)
        result = result.decode(encoding='ascii').lower()
        print('Installing Deos repo')
        subprocess.run(['sudo', 'helm', 'repo', 'add', 'deos', self.helm_chart_url.replace('^',token)])
        subprocess.run(['sudo', 'helm', 'repo', 'update'])
        if result.find('objectscale-helm-dev') == -1:
            print('Installing Objectscale helm dev repo')
            subprocess.run(['sudo', 'helm', 'install', 'objs-mgr', 'deos/objectscale-manager', '--set', 'global.registry=objectscale'])
            subprocess.run(['sudo', 'helm', 'install', 'deos/ecs-cluster', '--set', 'global.registry=objectscale', '--generate-name', '--set', 'storageServer.persistence.size=50Gi', '--set', 'performanceProfile=Micro', '--set', 'provision.enabled=True', '--set', 'storageServer.persistence.protected=True', '--set', 'enableAdvancedStatistics=False', '--set', 'managementGateway.service.type=NodePort', '--set', 's3.service.type=NodePort'])
            return



    def start_minikube_if_stoppped(self):
        try:
            result = subprocess.check_output('Minikube status', shell=True)
        except:
            print('Starting Minikube')
            os.system('sudo minikube start --vm-driver=none')


