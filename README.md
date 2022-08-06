# Visuquation
Visualization of physical known partial differential equations in 1D.
# Description
This application solves the Heat, Schrodinger, and one-directional wave equations in 1D. The solution displays on a GUI with an option to animate the solution or,
alternately, to plot each time step separately with the ability to view the next or previous time step plot. On the GUI, the user can set all the relevant parameters 
to the solution, choose the initial condition, etc.
# Liberies
- numpy
- matplotlib
- scipy
- tkinter
# Run and use the project
- Run main
- Choose an equation from the options menu located under the title "Choose equation".
- If the Heat equation is chosen, set all the parameters as you wish by the entries under the title "Please enter the following values".
  If you choose wave equation, do the same. In addition, you need to set the initial condition form and the parameters for the initial 
  condition with the relevant option menu and entries.
  If the Schrodinger equation is chosen, do the same as the wave equation. In addition, you need to set the potential type by the relevant option menu.
- Press the button "solve equation" to get your solution.  
- Notice that you have default values inside all the entries, but to choose the initial condition form and potential type, you must press the options menu!
  Also, all the values you enter must be floats or integers (nx and Number cycles must be integers). There are some more limitations on the values to avoid 
  unreasonable solutions, if you input something wrong, you will see a message on the screen that tells the limitations so you can fix your input easily. 
- To plot the solution on the screen, press the button "plot," then if you want to switch to the next plot or go back to the previous plot, press "next plot" or
  "previous plot" buttons, respectively.
- To animate the solution, press the button "animate", you can pause and resume the animation by pressing the button "pause/resume".
  <img width="929" alt="image" src="https://user-images.githubusercontent.com/102433115/183098970-701d70e2-53f5-4f83-ab00-778d7af9c5c7.png">
# Extra points for the user
- Avoid many actions and fast pressings on the GUI buttons, particularly the "solve equation" button. If you do so, the program will possibly work
  a little bit slow.
- If the program works slow, stop it and then run again.
- Enjoy and have a profitable experience!.  
# Producers
Reem Harel and Shaya Kahn.
