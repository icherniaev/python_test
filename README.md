# Test task for python language skills


# Directory Structure


```bash
├── data
│   ├── data.csv
├── src
│   ├── init.py
│   ├── data
│   │   ├── make_dataset.py
│   ├── functions
│   │   ├── functions.py
│   ├── visualization
│   │   ├── visualize.py
├── README.md
└── .gitignore
```

Your app's source code is nested beneath the `app` directory. This is where assets are served from in `debug` mode. Note that in most cases it is not necessary to setup a watch to re-compile languages and syntaxes including CoffeeScript, Sass, Stylus, Jade, and LESS as the development server will automatically do this for you in middleware. Note that in your index page, you should not include the `/app` prefix since the development asset server will treat it as the root.

```html
<!- Serves app/js/main.js-->
<script data-aero-build="debug" src="/js/main.js"></script>
```

For deployment, `yoke` assumes that all the files (including the index page) required to run in `release` mode have been written to a directory called either `dist` or `build` off the root. Grunt or Gulp both have good facilities for writing the outputs of a task to a different directory.