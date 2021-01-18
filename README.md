### Repetition Analysis in Israeli Music
We analyzed the repetitiveness of Israel music, and made the results accesible via a website:
https://glglstats.herokuapp.com/

We measure the repetitiveness of a song by the number of characters saved when it is compressed using an algorithm similar to LZ-77.
We then ranked all songs that had ever appeared in the yearly pop charts, as well as rank all artists against each other.  
The idea for this project was based on https://pudding.cool/2017/05/song-repetition/  

We added a second part, which is a visualization of the repetitions in a given song.
This idea was based on https://colinmorris.github.io/SongSim/#/about.
We plotted all of this using plotly with pandas.

The biggest technical challenge was obtaining the data for the project. Once we got that done, we were only left to designing the website.
We are not web developers, so the code is quite bad, but we eventually built using dash and bootstrap. On a related note, I hate CSS now. 


