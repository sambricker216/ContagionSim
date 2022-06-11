# ContagionSim
 
<p> ContagionSim is a program designed to model the spread of contagious diseases </p>

<h2> Credits </h2>
<p> This program was written in python and uses the Pygame API for the visual and interactive components. </p>
 
<h2> Functionality </h2>
<h3> Setup, Simulating, and Using </h3>
<p> Upon running the program, the GUI will load in. The left side has the actual visuals of the simualation, while the right side has several buttons, number displays, and text entry fields.</p>
<p> Each round of simulation has four steps: status updates, death, movement, and infections. The status updates stage make any necessary changes from the previous to each sample (a sample is a member of the population). The death stage sees if a sample meets the death condition (described below). If this happens, then that sample is removed from the array. The movement stage has each sample move in a random direction. The last stage is infect, where the currently infected samples can spread diseases to other nearby samples (formula explained below). </p>

<p>The GUI on the right has three clickable buttons: </p>
<ul>
 <li> Single Sim (runs one round of the simulation) </li>
 <li> Reset (resets the simulation to one with all ne samples and any updated user values) </li>
 <li> Multi Sim (runs 100 rounds of the simulation) </li>
</ul>

<p> Below the buttons are several displays of relevant statistics for the simulation, such as the current amount of living population, deaths/infection (as a percentage) and the total number of infections. The rigth hand side has several text entry fields for the user preferences. Those fields include initial amount of immune samples, the how fast the virus spreads (on a scale of 0 to 100), the number of rounds the virus lasts, the number of rounds a sample is immune to a the virus following infection (also known as cool down time), and how deadly the virus is (on a scale of 0 to 1000).
 
<h3> The Samples </h3>
<p> The population that the simulated virus is being exposed to is know as the samples. The samples serve as both hosts for the virus and the way that it spreads. </p>
<p> The samples have have a variety of states that represent their virus status: </p>
<ul>
 <li> Clean: A clean sample is one the does not have the virus. They are represented by being blue. </li>
 <li> Immune: Immune samples are those that have complete immunity. Effectivley, they are members of the population that are vaccinated (for the sake of the simulation, it is assumed the vaccination provides absolute immunity.) Immune sample are a teal color  </li>
 <li> Adapted: Adapted samples are those that have developed an immunity through repeated exposure. The more often sample is exposed to the virus, the less likely they are to catch it in the future. Adapted samples show their color when they are not in an infected stage. They begin with the Clean blue color and gradient to green as they develop more immunity. </li>
 <li>New Infected: A New Infected sample is one that has just received the virus but is not yet able to spread it or die from it. This best mimic a real life incubation period. The New Infected stage always lasts one round. Newly infected samples have a pink color. </li>
 <li>Infected: An infected sample is one that has the virus. they can both spread it and die from it. The length of this stage is determined by the user. They are red in color. </li>
 <li>Cool Down: Cool Down is the final stage. It represents when a sample finished the Infected stage and has a temporary immunity from catching the virus again. The length of this stage is determined by the user. Cool Down samples are yellow. </li>
</ul>
<h3> The Calculations </h3>
<p> Here are the formulas used to determine various features and events: </p>
<h4> Infection: </h4>
<p> The most important part of this simulation is the infection. There are two main factors that affect infections: distance and the probability of an infection. The distance is determined by getting the absolute distance between the infected sample and the target sample. If that value is less than 5, the spread rate is unchanged. If it is between 5 and 15, it is halved. If it is between 15 and 30, it is quartered. Any distance greater than 30 is outside the infection range. Infect chance is based on RNG. The formula is rand(0,99) * log<sub>4</sub>(amount of times infected + 4). An infection occurs if the infection chance is less than the spread rate. Spread rate is a user set variable. The main ideas behind the forumla is that the farther away a target is or the more times its been infected, the lower its chance of infection.</p>
<h4> Death Chance </h4>
<p> The other main calculation that has to occur is virus induced death. A death occurs when an rng between 0 and 999 is less than the death chance. Death chance is formualted by $\frac{deathRate}{infect time - coolDown Time + 1}$. The numerator, death rate, is a user determined value. The denominator how much time there is left in the infection. The earlier in the infection, the higher the odds of death. </p>
<h2> Visuals </h2>
The visuals and interactive portions (value setting, button clicking) are done through the pygame API.
