# Hydra and Neptune - Adversarial Testing of NIDS in SDN

This repository contains the code for the Hydra Adversarial Testing Tool as well as Neptune, a machine learning based network intrusion detection system (NIDS) for Software-Defined Networks (SDN).

For more details of this work, please see our [IEEE NFV-SDN 2019](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/192742980/1570562331_Hydra.pdf) article:

```
James Aiken and Sandra Scott-Hayward
"Investigating Adversarial Attacks against Network Intrusion Detection Systems in SDNs." 
IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN), pp. 1-7. IEEE, 2019.
```

If you fork this project for your own development, please credit the AdversarialSDN-Hydra Github project and reference the [IEEE NFV-SDN 2019](https://ieeexplore.ieee.org/abstract/document/9040101) article. Please read these [Contribution Rules](https://github.com/sdshayward/AdversarialSDN-Hydra/wiki#contribution-guidelines).

### - Main Neptune and Hydra TestManager package files located within the [App directory](https://github.com/sdshayward/AdversarialSDN-Hydra/tree/master/App)

<p align="middle">
  <img src="imgs/NeptuneProcess.png?raw=true" alt="Neptune Flow Process" width="400" />
 <img src="imgs/HydraProcess.png?raw=true" alt="Hydra Flow Process" width="400" />
</p>

### - [Hydra](https://github.com/sdshayward/AdversarialSDN-Hydra/tree/master/Hydra) and [TestingTool](https://github.com/sdshayward/AdversarialSDN-Hydra/tree/master/TestingTool) directories form the Django framework for the web application

<p align="center">
  <img src="imgs/HydraGUI.png?raw=true" alt="Hydra GUI" width="600" />
</p>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What tools/libraries you need to install the software and how to install them.  This project was based on Ubuntu 18.04 so that most of the installation commands are tailored towards this distribution.

If not using your own SDN, the Hydra and Neptune testbed was implemented with [Faucet](https://faucet.nz/) as an SDN controller and [Mininet](http://mininet.org/), which is included in the project files.
Faucet, however, does need to be installed with the following:

```
sudo apt-get install curl gnupg apt-transport-https lsb-release

echo "deb https://packagecloud.io/faucetsdn/faucet/$(lsb_release -si | awk '{print tolower($0)}')/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/faucet.list

curl -L https://packagecloud.io/faucetsdn/faucet/gpgkey | sudo apt-key add -

sudo apt-get update

sudo apt-get install faucet
```
To get Faucet to launch on system boot:
```
sudo systemctl daemon-reload
sudo systemctl enable faucet-service
sudo systemctl start faucet-service
```
or just start and stop the Faucet controller manually:
```
sudo systemctl start faucet-service
sudo systemctl stop faucet-service
```


[Mininet](http://mininet.org/)
```
sudo apt-get install mininet
```

[Nmap/Nping](https://nmap.org/docs.html) [hping3](https://linux.die.net/man/8/hping3)
```
sudo apt-get install nmap
sudo apt-get install hping3
```

[Django](https://www.djangoproject.com/)
```
sudo apt-get install python-django
```

[Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)
```
sudo apt-get install python-pandas
```

[scikit-learn](https://scikit-learn.org/0.16/install.html) [NumPy](https://docs.scipy.org/doc/numpy/reference/)
```
pip install -U scikit-learn
```

Install the [Argus](https://qosient.com/argus/downloads.shtml) server and clients.
That is, download the latest server tar.gz and latest clients tar.gz,
Extract them, and within each extracted directory perform:
```
./configure
make

sudomake install
```

You may need the following pre-requisites for Argus:
```
sudo apt-get install libpcap-dev
sudo apt-get install flex
sudo apt-get install bison
```


### Installation and Deployment

First, configure the SDN controller (Faucet) to mirror all network traffic on Mininet to a specific host for Argus to listen to.

Add the [faucet.yaml](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/master/faucet.yaml) file to /etc/faucet/
Faucet will require a restart ```sudo systemctl restart faucet-service```

This mirrors all traffic to host 10. However, it can be configured differently, if required.  Just make sure to tell Argus to listen to the different host.

Next, navigate to the base directory AdversarialSDN-Hydra and execute the following command to start the Hydra web application server and database:

```
sudo python manage.py runserver
```

To clear the database, you can use:

```
sudo python manage.py flush
```

At this point, you should be able to load the testing tool at the following address in your browser:
```
http://127.0.0.1:8000/
```
## Running the tests

    1. Choose the network configuration you would like to use for the test.
    2. Configure the test you would like to perform. All fields must be configured before submission.
    3. Select submit test.
    
You will see the test processes commence in consoles. These will disappear when the result has returned and will appear in the testing results table in the interface.

## Generating your own Flow Statistics to train Neptune
This repository only comes with a small selection of sample flow statistics in App/stats_training and App/stats_testing (as well as in App/tests/test_stats/).  The details of the training datasets we used are provided in the paper. Unfortunately, we cannot make these available as the DARPA dataset is restricted access. To generate your own flow statistics for Neptune to use in training and testing, you can use [App/Neptune/traffic_stats.py](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/master/App/Neptune/traffic_stats.py).  This class is the flow statistic generation class used by Neptune itself. However, it can also be used standalone to generate your own statistics.

As mentioned in the Installation instructions, Argus is required for flow statistic generation.  Mininet and Faucet will need to be started up manually as Argus will listen to s1-eth0 by default. However, this can be [changed](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/4cbb585eef9856b290bb5eb09cdbd6b450811e11/App/traffic_stats.py#L89) based on your personal setup.  The python script for Hydra launches Mininet [like so](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/f4de6cd9197c2eff6417f2b43d0a20e929bbeeef/App/TestManager/main.py#L185). An equivalent can be launched manually via the command line.

```
sudo mn --topo single,10 --controller remote,ip=127.0.0.1,port=6653
```
Note that the SDN controller is set to remote on port 6653, which is where Faucet should be running.

The Class can be started by executing:
```
sudo python traffic_stats.py
```
When recording your benign traffic, set [self.malicious = 0](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/4cbb585eef9856b290bb5eb09cdbd6b450811e11/App/traffic_stats.py#L57)

When recording malicious traffic set [self.malicious = 1](https://github.com/sdshayward/AdversarialSDN-Hydra/blob/4cbb585eef9856b290bb5eb09cdbd6b450811e11/App/traffic_stats.py#L57)

(This labels your flows so that the ML models can use them (supervised learning).)


## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Faucet](https://faucet.nz/) - SDN Controller

## Installation Troubleshooting

1. If the curl command for packagecloud.io remains at 0%, the packagecloud servers may be down and you may have to wait until they have recovered
2. If the application is crashing due to missing files/directories, double check the naming of the directories within the code with the ones on your local environment to ensure that they are consistent. 

## Tests
Execute any tests within ../tests/ directories from the ../AdversarialSDN-Hydra directory.
e.g.
```
cd <your-directory>/AdversarialSDN-Hydra
sudo python App/Neptune/tests/test_unit_main.py
```

## Contributors

* **James Aiken**
* **Sandra Scott-Hayward**

To get in contact about the project, please email James at jaiken06@qub.ac.uk 

## Acknowledgments

* Initial inspiration for format of Neptune code taken from [Chandrahas' Simple IDS using Ryu](https://github.com/Chandrahas-Soman/Simple_IDS_using_RYU_SDN_controller_and_Machine_Learning/blob/master/IDS_RyuApp.py)
* Hydra front end design based on Traversy Media's [Tutorial](https://youtu.be/Wm6CUkswsNw)
