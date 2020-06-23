import os
import subprocess

class objectscale_utility:
    # TODO: find correct URL, if applicable.
    helm_chart_url = "https://^@raw.githubusercontent.com/emcecs/charts/master/docs"
    # TODO: find correct installlation path
    objectscale_install_path = ''
    objectscale_path: str
    is_valid_install: bool

    def __init__(self):
        self.objectscale_path = ''
        self.is_valid_install = False

    def check_objectscale_installation(self, PATH=os.getenv('PATH')) -> bool:
        print('Verifying objectscale Installation.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('Helm repo list', shell=True)
        result = result.decode(encoding='ascii').lower()
        if result.find('ecs-cluster') == -1:
            print('ECS-cluster not installed')
            return False
        if result.find('objectscale-manager') == -1:
            print('Objectscale not installed')
            return False
        print('All objectscale components running, Install not necessary')
        return True


    def get_objectscale_version(self):
        print('objectscale version.')
        self.start_minikube_if_stoppped()

    def clean_objectscale(self):
        print('Cleaning objectscale.')
        self.start_minikube_if_stoppped()
        print('objectscale Cleaned.')

    def uninstall_objectscale(self):
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('Helm list | awk "{print $0}"', shell=True)
        result = result.decode(encoding='ascii').lower()

        print('Uninstalling objectscale.')

    def install_objectscale(self, token: str, PATH=os.getenv('PATH')):
        print('Installing objectscale.')
        self.start_minikube_if_stoppped()
        result = subprocess.check_output('Helm repo list', shell=True)
        result = result.decode(encoding='ascii').lower()
        if result.find('deos') == -1:
            print('Installing deos repo...')
            os.system('helm repo add deos '+self.helm_chart_url.replace('^',token))
            os.system('helm repo update')
        if result.find('objectscale-helm-dev') == -1:
            print('Installing objectscale...')
            os.system('helm install objs-mgr deos/objectscale-manager --set global.registry=objectscale')
            os.system('helm install deos/ecs-cluster --set global.registry=objectscale --generate-name --set storageServer.persistence.size=100Gi --set performanceProfile=Micro --set provision.enabled=True --set storageServer.persistence.protected=True --set enableAdvancedStatistics=False --set managementGateway.service.type=NodePort --set s3.service.type=NodePort')
            return



    def start_minikube_if_stoppped(self):
        result = subprocess.check_output('Minikube status', shell=True)
        result = result.decode(encoding='ascii')
        if result.lower().find('host: running') == -1:
            print('Starting Minikube')
            os.system('minikube start')


