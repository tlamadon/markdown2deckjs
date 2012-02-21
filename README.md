# markdown2deckjs

Modified: Thibaut Lamadon -- Added MathJax support
          John McDonnell -- Various cleanup

Version: 0.1 | 2011/09/21

## What is this?

This is a simple modification of Ulf Bögeholz version. 
I just added support for math with MathJax. I am leaving most of the author's comment.

After I saw deck.js recently, I immediatelly liked the look and feel of it. 
What I did not like was to generate HTML slides by hand. I surfed around a bit and quickly found 
out that there was a nice markdown library for python. Playing around (and not sleeping instead) 
quickly showed results. Voila.

## Dependencies

* markdown
* jinja2
* elementtree

Install by using Pip: `pip install markdown jinja2 elementtree`

## How to use

* Write a markdown file with your presentation in it
* Compile the markdown file to a deck.js HTML file
* Enjoy the slides

### Play-by-play

    $ git clone https://github.com/ulf/markdown2deckjs.git
    $ cd markdown2deckjs
    $ ./m2d README.md templates/plain.html "Readme" > readme.html
    # Look at the readme.html file in your browser. Done

## How do I create my slides?

Every time the markdown contains a H1 or H2 (#, ##), a new slide will be created in your presentation. Basically just write your text and mix in a heading if you need a new slide.

    # Title Slide
	
	  ## First Content Slide
	  This is nice
	
	  ## Second Content Slide
	  This too

    ## Slide with some math
    
      - Here it is $\alpha$
      - ~ And more $\int x dx$
    
     ~ $$ g(z) = \int f(a-z) u(a) da $$    


will result in a four-slide presentation with rendered math. Try it:
  
    $ m2d example1.md templates/plain.html "My Test" > example1.html


## Downloadable files

One problem with deck.js is that it is not easily sharable offline. So I added an option to the program which allows for creation of simple HTML files for easy distribution. No slide effects will be applied in the HTML code, as well other control elements (like tilde, see below) will be stripped.

    $ m2d example.md templates/download.html "My Test" -p > downloadable.html

## Seems like magic. How does it work?

The python markdown module offers a broad scope for writing extensions. I found a possibility to hook in an extension after the HTML element tree has already been generated from the markdown file. All I do is traverse the tree and make some minor adjustments in the element configuration. The altered HTML is then pasted into a plain deck.js template to generate the presentation.

## Differences to markdown

I added a little feature to make slides more interactive. If your text elements end with a tilde, the char is stripped and the element is instead given the `slide` class, which has the effect that the element will not be shown initially. Instead, you need to advance the slide to show the element. This seemed to be te easiest way to construct incremental slides.

## I want to extend this

Feel free! Just fork or get in touch if you like, there might be a lot of ways to make this better.

