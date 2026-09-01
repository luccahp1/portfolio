<!--
  This is the profile README, not the portfolio site's.

  Copy the four files next to it (README.md, contrib-heatmap.svg,
  ascii-portrait.svg, info-card.svg) into the root of the luccahp1/luccahp1
  repo, along with .github/workflows/update-profile-art.yml, and GitHub renders
  it at the top of the profile page. The image paths are relative, so they work
  in both places.

  Everything that moves is SMIL or CSS keyframes inside the SVGs. GitHub strips
  <script> from READMEs and sanitizes inline CSS, but it renders SVGs embedded
  with <img> and plays their animations. That constraint is the whole design.

  Widths are load-bearing: 370 + 490 = 860, so the portrait and the card line up
  with the heatmap's edges. Only <br> gives vertical space here; style="" is
  stripped, and <h1>/<h2> draw a full-width rule, which is why every heading
  below is an <h3>.
-->

<div align="center">

<h3><code>lucca@github ~ $ ./contributions.sh</code></h3>

<img src="./contrib-heatmap.svg" width="860" alt="A year of contributions, revealed box by box. Refreshed daily." />

<br><br>

<h3><code>lucca@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top"><img src="./ascii-portrait.svg" width="370" alt="ASCII art portrait" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" alt="Role, stack, and what I am building" /></td>
  </tr>
</table>

<br>

<h3><code>lucca@github ~ $ cat links.txt</code></h3>

<a href="https://luccahp1.github.io/portfolio/">portfolio</a> ·
<a href="https://luccahp1.github.io/portfolio/resume.html">resume</a> ·
<a href="mailto:luccaprada25@gmail.com">email</a>

<br><br>

<sub>
No stats services and no token. Three Python scripts draw these SVGs, a cron
scrapes the public contribution calendar every morning, and the art is committed
to the repo, so nothing here can go down or rate-limit on me.
<a href="https://github.com/luccahp1/portfolio/tree/main/scripts">Source.</a>
</sub>

</div>
