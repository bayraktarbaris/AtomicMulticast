Name: Orhun Buğra Baran No: 2035699
Name Barış Bayraktar  No:2035715

In order to run the experiments you need to type sudo python topology.py numberOfnodes lossRate multicastSenderHostId experimentNo

Some experiments are not in the exact form that is mentioned above. For the experiments that is run for different number of group members you need to rerun the experiment with the different numberOfNodes variable. In some experiments especially the ones that we put packet loss if you want to simulate those be aware that they will not give you the exact same behavior. However, overall behavior should be same as provided in the project report. Sometimes if you run some experiments back to back VM behaves differently some applications crashes(especially if you are sending so many packets with long delays, probably the number of processes working on hosts is getting too much for VM to handle, therefore logs may not be not created properly and queues may not be consistent) Therefore running those experiments again after closing and reopening the VM is suggested(at least worked for us).

After completing the experiments run the scripts experiment + experimentNo + .py for example, after experiment 1: python experiment1.py 
If you want to see the experiment results for different number of Group size or for different lambda you need to adjust the file names in the experiment.py file accordingly. Otherwise it will give an error since file wont be found.