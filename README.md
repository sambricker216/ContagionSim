# ContagionSim
 
<p> ContagionSim is a program designed to model the spread of contagious diseases </p>

<h2> Credits </h2>
<p> This program was written in python and uses the Pygame API for the visual and interactive components.
 
<h2> Functionality </h2>
<h3> Setup, Simulating, and Using </h3>
<p> Upon running the program, the GUI will load in. The left side has the actual visuals of the simualation, while the right side has several buttons, number displays, and text entry fields.</p>
<p> Each round of simulation has four steps: status updates, death, movement, and infections. The status updates stage make any necessary changes from the previous to each sample (a sample is a member of the population). The death stage sees if a sample meets the death condition (described below). If this happens, then that sample is removed from the array. The movement stage has each sample move in a random direction. The last stage is infect, where the currently infected samples can spread diseases to other nearby samples (formula explained below). </p>
<p>The GUI on the right has three clickable buttons: 
