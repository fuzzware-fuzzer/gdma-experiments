#!/bin/bash

if [ "$#" -ne 1 ]; 
then
	echo "Missing command: Please give base directory of results"
	exit
fi
echo "received basedir for dice & p2im results is $1"
cd $1
cd DICEFuzzBase
if [ -d Oscilloscope ];
then
	rm -r Oscilloscope
fi
if [ -d ModbusRedZones ];
then
	rm -r ModbusRedZones
fi
if [ -d GPSReceiver ];
then
	mv GPSReceiver GPS-Receiver
fi

if [ -d GuitarPedal ];
then
	mv GuitarPedal Guitar-Pedal
fi

if [ -d MIDISynthetizer ];
then
	mv MIDISynthetizer MIDI-Synthesizer
fi

if [ -d SolderingStation ];
then
	mv SolderingStation Soldering-Station
fi

if [ -d StepperMotor ];
then
	mv StepperMotor Stepper-Motor
fi
cd -


cd P2IMFuzzBase
if [ -d Oscilloscope ];
then
	rm -r Oscilloscope
fi
if [ -d ModbusRedZones ];
then
	rm -r ModbusRedZones
fi
if [ -d GPSReceiver ];
then
	mv GPSReceiver GPS-Receiver
fi

if [ -d GuitarPedal ];
then
	mv GuitarPedal Guitar-Pedal
fi

if [ -d MIDISynthetizer ];
then
	mv MIDISynthetizer MIDI-Synthesizer
fi

if [ -d SolderingStation ];
then
	mv SolderingStation Soldering-Station
fi

if [ -d StepperMotor ];
then
	mv StepperMotor Stepper-Motor
fi
cd -
