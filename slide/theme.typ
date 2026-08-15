#let wine = rgb("#8E1F1F")
#let red = rgb("#C12720")
#let ink = rgb("#251D1B")
#let cream = rgb("#F7F0ED")
#let blush = rgb("#EEDDD8")
#let sand = rgb("#E6DED4")
#let gold = rgb("#C89A35")
#let muted = rgb("#756965")

// 16:9 layout grid: 0.58in side margins, 1.35in content start,
// and a protected footer baseline at 7.26in.
#let margin-x = 0.58in
#let content-w = 12.173in
#let content-y = 1.35in
#let gap = 0.18in

#let footer(n) = place(
  bottom + left,
  dx: 0.46in,
  dy: -0.24in,
  text(size: 8pt, fill: muted)[Invisible BSRS｜Build with AI Hackathon],
) + place(
  bottom + right,
  dx: -0.46in,
  dy: -0.24in,
  text(size: 9pt, fill: muted)[#n],
)

#let brand() = place(top + right, dx: -0.46in, dy: 0.31in)[
  #align(right)[
    #text(size: 9pt, weight: "bold", fill: wine)[INVISIBLE]
    #linebreak()
    #text(size: 6.5pt, tracking: 1.6pt, fill: wine)[BSRS]
  ]
]

#let head(no, title, en, n) = {
  place(top + left, dx: 0.46in, dy: 0.42in)[
    #grid(columns: (0.28in, auto), column-gutter: 0.12in,
      line(length: 0.28in, stroke: 1.2pt + ink),
      block[
        #text(size: 25pt, weight: "bold", fill: ink)[#no、#title]
        #linebreak()
        #text(size: 7.2pt, weight: "bold", tracking: 1.4pt, fill: muted)[#en]
      ]
    )
  ]
  brand()
}

#let panel(body, fill: white, height: auto, inset: 18pt, radius: 7pt, stroke: none) = block(
  width: 100%, height: height, fill: fill, inset: inset, radius: radius, stroke: stroke, body
)

#let deck-grid(..args) = block(width: content-w, grid(..args))

#let tag(body, fill: red) = box(fill: fill, radius: 12pt, inset: (x: 14pt, y: 6pt))[
  #text(size: 12pt, fill: white, weight: "bold")[#body]
]

#let bullet(body) = grid(columns: (9pt, 1fr), column-gutter: 8pt,
  circle(radius: 3.2pt, fill: wine),
  text(size: 15pt)[#body]
)
