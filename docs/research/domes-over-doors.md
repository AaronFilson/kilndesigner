# Domes over a door: statics, openings and thrust

Checked: 2026-10-28. Scope: sail domes (a sphere through the four top corners of a rectangular
chamber) over studio kiln chambers about 2 to 4 ft across, cast in insulating castable or laid
in brick, with a door in one wall. Every number has a source tag like [D3]. The tags are listed
under "Sources" at the end.

How values are marked (as in `kiln-hardware.md`):
- **Verified** means I read it on the page or in the PDF text itself.
- **Excerpt** means I saw it only in a search-engine snippet, a full-text-search snippet or a
  publisher's summary.
- **Derived** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a forum post or similar, passing on practice rather than a design rule.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Notes on the sources:
- PDFs were read as text with `pypdf`. The 1940 Timoshenko scan's OCR garbles the formulas; the
  formulas were read in the 2nd edition's OCR text, and the two editions' prose agrees.
- Heyman's *The Stone Skeleton* (1995), Denzer's *Build Your Own Earth Oven*, Olsen's *The Kiln
  Book* and Rhodes' *Kilns* are borrow-only scans on the Internet Archive. They were read through
  its full-text search, which returns about a line around each hit. Quotes from them are stitched
  from overlapping snippets and marked Excerpt; "…" marks a gap between snippets.
- Forno Bravo's own pages and PDFs returned HTTP 403 or a bot-check page. Its figures come from
  search summaries (Excerpt). Its forum pages could be read (secondary).
- Searched and found to have no dome-thrust method: HarbisonWalker's *Brick Installation Guide*
  (2008) [D10] and *Modern Refractory Practice* (1950, full-text search) [D10], and Trinks'
  *Industrial Furnaces* (1925, 1926, 1951) [D23]. HarbisonWalker says only that "Combinations of
  these shapes taper in two dimensions to turn domes" (p. 12) and that its engineers' computer
  programs "can produce complex arch or dome design parameters" (p. 18) [D10] Verified.
- No kiln or oven maker states a rule for a dome over a door. The rule in §D7 is derived from
  Heyman's method and HarbisonWalker's arch limits, and is marked Derived throughout.

Cross-references: this section adds to `combustion-and-masonry.md` §6.4–6.7 (cast arches,
sprung-arch geometry, catenary statics, dome geometry) and `kiln-hardware.md` §4.3–4.6
(HarbisonWalker's arch method; its [S20] is [D10] here) and §6 (doors). It does not repeat them.

Notation for §D2–D7: chamber inside width 2a, depth 2b, half-diagonal c = √(a² + b²), rise f,
sphere radius R = (c² + f²)/2f (`combustion-and-masonry.md` §6.7). φ is the angle from the crown
on the sphere; φc is the corners' angle, cos φc = (R − f)/R. q is the dome's weight per unit area
of its surface (Σ density × thickness of its layers). t is the structural (castable or brick)
thickness. The door, when there is one, is in a wall of width 2a at y = +b.

---

## D1. Membrane theory of a spherical dome under its own weight

| Item | Value | Mark | Source |
|---|---|---|---|
| Meridional force | N_φ = −aq(1 − cos φ)/sin²φ = −aq/(1 + cos φ), with a = sphere radius and q = weight per unit area. "It is seen that the forces N_φ are always negative. There is thus a compression along the meridians that increases as the angle φ increases." | Verified | [D1] §106, eq. (257) |
| Hoop force | N_θ = aq (1/(1 + cos φ) − cos φ) | Verified | [D1] eq. (257) |
| Crown and equator | "For φ = 0 we have N_φ = −aq/2, and for φ = π/2, N_φ = −aq. The forces N_θ are also negative for small angles φ." Worked example: hoop force at the top −37.5 kN/m = −γtR/2 | Verified | [D1] [D2] |
| Hoop transition | "When 1/(1 + cos φ) − cos φ = 0, i.e., for φ = 51°50′, N_θ becomes equal to zero and, with further increase of φ, becomes positive. This indicates that for φ greater than 51°50′ there are tensile stresses in the direction perpendicular to the meridians." | Verified | [D1] |
| Supports | The membrane stresses are accurate "if the supports are of such a type that the reactions are tangent to meridians". "Usually the arrangement is such that only vertical reactions are imposed on the dome by the supports, whereas the horizontal components of the forces N_φ are taken by a supporting ring". This causes "some bending of the shell ... near the supporting ring", which in a thin shell "is of a very localized character" | Verified | [D1] |
| Ring force | "The ring at the edge is supported vertically and it is unsupported radially. The opposite of the horizontal component of the meridian force loads the ring." Ring tension "H = a0 p_p = a0 N_α cos α0", a0 being the base-circle radius. Worked: R = 10 m, α0 = 60°, t = 0.3 m, γ = 25 kN/m³ give N_α = −50 kN/m at the base and −37.5 at the top, hoop force +12.5 kN/m at the base, ring force 216.5 kN | Verified | [D2] |
| Masonry with no tension | Lau's lower-bound thrust-line method "finds satisfactory equilibrium solutions for α ≤ 51.8° for all t/R ratios considered in this study" (down to t/R = 0.001). "Similar to arches, shallow domes thrust more than deeper domes, relative to self weight" | Verified | [D3] pp. 48, 51 |
| Very shallow domes | "hoop forces become less critical because the curvature of the line of thrust approaches a straight line. The horizontal thrust at the crown and base clamp the masonry units in place in the lune, similar to a flat arch, thus stabilizing the dome with minimal or no hoop forces" | Verified | [D3] p. 54 |
| Thrust at the base | "the dome and support structure must also resist the horizontal component, the outward thrust, particularly near the base of the dome where total thrust is greatest. External means of resistance may be employed, such as massive support structure walls, as used in the Roman Pantheon, or a metal tension ring around the dome's base" | Verified | [D3] p. 14 |
| Minimum thickness, complete hemisphere | Heyman: "… is 4.2 per cent of the radius, that is, t/R = 0.042. This required minimum thickness falls sharply if the dome does not embrace a full 180°" | Excerpt | [D4] §3.5 |
| — later estimates | Lau: 0.069 with no hoop force between lunes, 0.041 with hoop forces. Nodargi & Bisegna, refined: "0.04284 times the radius of the mid-surface" | Verified | [D3] pp. 54–55; [D9] |
| Minimum thrust of a hemisphere | "For a lune of a hemispherical dome of sufficient thickness, the modified thrust line method estimates the minimum thrust to be about 20% of the lune's weight" | Verified | [D3] p. 51 |
| Shell against arch | "Unlike an arch, a dome can be thought of as a thin shell, with forces acting smoothly within its surface." The chapter summary adds (paraphrased by the fetch tool) that minimum thickness is set mainly by local buckling and that complete domes can be thinner than incomplete ones | Verified (first sentence); Excerpt (rest) | [D4] Ch. 3 page |

Reactions per unit length of the base circle at φ0 **(Derived)** by resolving N_φ(φ0) at the edge:
- Vertical V = qR sin φ0/(1 + cos φ0). Horizontal outward thrust H = qR cos φ0/(1 + cos φ0)
  (the reaction runs along the meridian, so H/V = cot φ0).
  A ring at the base carries T = H × R sin φ0 = qR² sin φ0 cos φ0/(1 + cos φ0).
- Check against [D2]: q = 25 × 0.3 = 7.5 kN/m², R = 10 m, φ0 = 60°. Then H = 7.5 × 10 × 0.5/1.5 =
  25 kN/m and T = 25 × 8.66 = 216.5 kN, as printed.
- Check: V × 2πR sin φ0 = 2πR²q(1 − cos φ0), the cap's weight, which is Timoshenko's resultant
  "R = 2πa²q(1 − cos φ)" [D1].
- Shallow cap (φ0 small): H → qR/2. With span L (diameter) and rise f, R ≈ L²/8f, so
  H ≈ qL²/16f. That is half the thrust wL²/8f of a parabolic arch of the same span and rise
  carrying w = q per unit length.
- No hoop tension anywhere when φc ≤ 51.83°. For a sail dome f/c = (1 − cos φc)/sin φc =
  tan(φc/2), so this holds when f ≤ tan 25.9° × c = **0.486 c**.

---

## D2. Sail dome on four walls (no door in a wall it bears on)

Cut by the four wall planes, the membrane field of §D1 is an equilibrium state, and by the safe
theorem (§D3) it is enough to show the dome stands. Each wall must supply the traction the field
needs along its top arc: an outward horizontal thrust, a vertical load, and a shear along the
arc **(Derived)**. The field contains no tension only when φc ≤ 51.8°, that is f ≤ 0.486 c.

Derived results:
- **Total outward thrust on a wall = H_c × the wall's inside length**, where H_c =
  qR cos φc/(1 + cos φc) is the full cap's base thrust at the corners' angle (§D1). So the
  average thrust per unit length is H_c on every wall. Proof: the part of the full cap beyond the
  wall is in equilibrium. Its base reactions have a horizontal, radial component of H_c per unit
  length; their components normal to the wall add up to H_c × the chord, which is the wall's
  length; and its weight is vertical. So the wall's cut must carry the same total.
- The thrust peaks at mid-wall and falls toward the corners. The shear along the top of each wall
  is zero at mid-wall and largest at the corners, where it drags the wall's top toward the corner
  and down. That is how a sail dome on walls sends load toward its corners (the pendentive
  action). The vertical load is spread fairly evenly along each wall. The table's numbers come
  from integrating the membrane field along each wall arc; the vertical reactions add up to the
  dome's weight (check).
- On open sides (a dome on four columns), Timoshenko notes that the membrane solution leaves
  "shearing forces N_θφ which do not vanish at the edge of the dome", and that "so long as we
  limit ourselves to membrane theory, we shall not have enough constants to satisfy all the
  conditions … In actual constructions a reinforcing ring is usually put along the edge of the
  shell to carry the shearing forces" [D1] §111 Verified. A kiln's continuous walls do that job.
- Rectangular frame around the wall tops: each member along the side walls carries tension equal
  to half the front wall's total thrust, and the reverse. Each member also bends under its own
  wall's thrust between the corner posts (bending as in `kiln-hardware.md` §4.5).

Worked example **(Derived)**: the repo's `examples/dome-castable-kiln.yaml`. Chamber 30 × 36 in,
rise 8 in. Lining: Kast-O-Lite 30 LI Plus, 3 in at 92 lb/ft³ (after 1,500 °F,
`combustion-and-masonry.md` §6.1), under 2 in of 8 pcf blanket. q = 23.00 + 1.33 = 24.33 lb/ft²
of surface. c = 23.43 in, R = 38.31 in, φc = 37.70°, f/c = 0.341. Shell area 8.04 ft² over
7.50 ft² of plan; weight 195.7 lb.

| Wall | Total thrust | Average | Thrust at mid-wall / corner | Total vertical | Vertical at mid-wall / corner | Shear along the top at the corner |
|---|---|---|---|---|---|---|
| 30 in (front, back) | 85.8 lb | 34.3 lb/ft | 36.4 / 26.6 lb/ft | 49.3 lb | 19.4 / 18.3 lb/ft | 12.6 lb/ft |
| 36 in (sides) | 102.9 lb | 34.3 lb/ft | 37.2 / 23.7 lb/ft | 48.6 lb | 15.8 / 14.6 lb/ft | 11.6 lb/ft |

- H_c = 24.33 × 3.193 ft × cos 37.70°/(1 + cos 37.70°) = 34.3 lb/ft, the average in both rows.
  qR/2 = 38.8 lb/ft.
- Frame: the side members carry 42.9 lb of tension, the front and back members 51.5 lb.
- At f = 12 in (φc = 54.2°, past 51.8°) the field has hoop tension in the shell near the corners,
  although the walls are still pushed outward there (8 and 4 lb/ft). At f = 20 in it also pulls
  the walls inward at the corners (−20 to −25 lb/ft). Masonry can do neither. Above
  f = 0.486 c, use the sliced state of §D4 instead.

---

## D3. Safe theorem, slicing, and the minimum thickness of arches

| Item | Value | Mark | Source |
|---|---|---|---|
| Safe theorem | "If a line of thrust can found which is in equilibrium with the external loads and which lies wholly within the masonry, then the structure is safe. …[T]he line of thrust found in order to satisfy the safe theorem need not be the actual line of thrust[.]" (Heyman 1996, p. 6, quoted) | Verified | [D3] p. 18 |
| — in three dimensions | "if a compression-only network can be found that fits within the boundaries of a vault, then the vault will stand in compression. Note that if we want a solution without any tension (hinges) in the section, we want the solution to lie within the middle third of the section" | Verified | [D7] p. 5 |
| Minimum and maximum thrust | the possible equilibrium states run from the minimum (passive) thrust, "the least amount this vault will push sideways onto its neighboring elements", to the maximum (active) thrust, "the largest horizontal force this vault can provide" | Verified | [D7] p. 5 |
| Slicing | domes treated "as composed of a series of distinct segments or slices or 'lunes' … since the equilibrium of each slice is investigated separately, if it can be shown that each element of the sliced structure is stable, then it is argued that the original structure must be stable." "The similarity between the 'settore solido' of Poleni and the 'orange slice' of Heyman is very clear." | Verified | [D8] |
| — conservative | "A compressive-only stress state in the dome is naturally accomplished by a sliced equilibrium model … the sliced equilibrium model is not completely adequate … because it neglects the beneficial static effects due to the dome shell behavior." "the slicing technique does not consider the hoop compressive stresses building up in the upper part of the cap" | Verified | [D9] p. 2; [D22] abstract |
| — for thrust | Heyman: the slicing technique "may be used to give general indications of significant quantities, for example the horizontal thrust"; "there is a horizontal thrust in the sliced arch which must somehow be contained" | Excerpt | [D4] Ch. 3–4 |
| Geometrical factor of safety | "The ratio of the actual thickness to this minimum is the 'geometrical factor of safety'." "Often it exceeds 2, but by the so-called 'safe' theorem, if it exceeds 1 then the arch is safe." | Verified | [D4] Ch. 2 page |
| — practical value | "safe practical values for the geometrical factor of safety in arch construction seem to be about 2" | Excerpt | [D4] §2.2 |
| — middle third and half | with the thrust line in the middle third of a rectangular section the factor is three; in the middle half, two. "Heyman suggests that for arches or ribs the geometrical factor of safety should be greater than two" | Verified | [D6] §5 |
| — HarbisonWalker | "The line of thrust in a cold arch should lie within the middle third of the brick" (already in `kiln-hardware.md` §4.3) | Verified | [D10] p. 16 |
| Minimum thickness of a circular arch under its own weight (Couplet–Heyman), half-angle α, η = t/r (r = centre-line radius) | α = 60°: η = 0.0227694 (Heyman), 0.0228482 (CCR), 0.0228489 (Milankovitch). α = 90°: 0.105965, 0.107426, 0.107478. α = 120°: 0.314124, 0.326547, 0.327607. Haunch hinge at α = 90°: 58.83° (Heyman), 54.50° (CCR), 54.48° (Milankovitch). Thrust h = H/(wr) at 90°: 0.621 | Verified | [D5] Table 1 |

**Derived: minimum thickness at other half-angles.** A numerical solver of the same problem
finds the thinnest arch that contains some thrust line. The thrust line cuts the radial joint at
angle θ at radius ρ(θ) = (h y0 + g(1 − cos θ))/(h cos θ + θ sin θ), with r = 1 and w = 1, crown
thrust h at height y0. g = 1 puts the weight on the centre line (CCR); g = 1 + η²/12 uses the true
centroid of the voussoirs (Milankovitch). It reproduces [D5] Table 1 to every printed digit at
60°, 90° and 120° (η, and h). Values (CCR; Milankovitch agrees to four decimals up to 70°, and is
0.107478 at 90°):

| α | 10° | 20° | 25° | 30° | 35° | 40° | 45° | 50° | 55° | 60° | 65° | 70° | 75° | 80° | 85° | 90° |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| η_min | 0.00002 | 0.00031 | 0.00074 | 0.00153 | 0.00280 | 0.00473 | 0.00750 | 0.01129 | 0.01634 | 0.02285 | 0.03107 | 0.04126 | 0.05368 | 0.06864 | 0.08643 | 0.10743 |

**Derived: one formula behind HarbisonWalker's thrust constants.** Take a circular arch of
centre-line radius r and half-angle α (half the central angle θ), weight w per unit length of
centre line, with the thrust line at mid-thickness at the crown and at the skewbacks (the
assumption of the HW constants [D10]). Moments about the skewback give

  H = w r (α sin α − 1 + cos α)/(1 − cos α),  V = w r α (half the weight W = 2 w r α).

This gives H/W = 1.486, 0.980, 0.911, 0.723, 0.621 and 0.461 at 1, 1½, 1.608, 2, 2.302 and
3 in/ft. HarbisonWalker's table (`kiln-hardware.md` §4.3) prints 1.49, 0.98, 0.91, 0.72, 0.62,
0.46. The centre-line thrust line strays from the centre line by at most 0.0015 r at 1.608 in/ft
and 0.014 r at 3 in/ft, inside any practical middle third.

---

## D4. Openings: a dome with a free edge

| Item | Value | Mark | Source |
|---|---|---|---|
| Heyman, half dome | the symmetrical membrane solution "would be valid for the half dome only if the free edge were subjected to the compressive and tensile forces shown. No simple membrane solution …". "Nevertheless it is clear intuitively that a half dome will stand if it has sufficient thickness, and a safe estimate of this thickness may be made by using again …". "… theorem, once again, confirms that, if the sliced half dome stands, then so will the half dome itself. The problem, then, is to determine the minimum thickness necessary for the stability of a semicircular arch …". Fig. 3.14: "Half dome sliced into parallel arches." | Excerpt | [D4] §3.6 "Incomplete hemispheres", pp. 41–42 |
| — free edge | "boundary conditions (e.g. for the half dome the 'free' edge must be supported as shown in fig. 3.6). On the other hand a safe …" | Excerpt | [D4] Ch. 3 |
| Heyman, incomplete shells | "incomplete shells have edges. The behaviour of incomplete shells can be different from that of complete shells; certainly the decapitated egg is more flexible than the uncut …". Fig. 3.13: "Required minimum thicknesses for incomplete domes" (the values could not be read) | Excerpt | [D4] §3.6 |
| Half dome standing free | "The half dome in fact can stand freely, and will also be stable when subjected to the out-of-balance horizontal …" (the context is half domes buttressing a main dome, indexed as "half dome as buttress 43") | Excerpt | [D4] §3.6 |
| Edge members | on isolated supports, "a reinforcing ring is usually put along the edge of the shell to carry the shearing forces" | Verified | [D1] §111 |
| Incomplete shallow domes, as built | Pines Calyx, Dover (2005–06): "Both domes are incomplete: the upper dome surface has a lens-shaped cutout while the lower dome intersects the cylindrical support wall of the upper dome"; checked by membrane theory and thrust lines | Verified | [D3] pp. 94–98 |
| Flat roofs | a flat vault "withstands mainly vertical loads … discharging them at its boundary by means of a vault effect, i.e., with a horizontal thrust" | Verified | [D21] p. 657 |

### D4.1 A sail dome with a door, sliced into parallel arches (Derived)

This applies Heyman's half-dome slicing to a sail dome.

1. Slice the dome with vertical planes parallel to the door wall. Each slice is an arch spanning
   between the two walls perpendicular to the door wall (the "bearing walls"). It needs nothing
   from the door wall or the wall opposite it. By the safe theorem, if every slice stands, the
   dome stands.
2. The slicing planes are parallel and the intrados and extrados are concentric spheres, so each
   slice is a circular arch of uniform thickness in its own plane. At distance y from the centre
   (|y| ≤ b):
   - intrados radius ρi = √(R² − y²); extrados ρe = √((R + t)² − y²);
   - thickness ts = ρe − ρi. It is never less than t, and it grows toward the door because the
     plane cuts the shell obliquely;
   - centre-line radius rs = (ρi + ρe)/2; half-angle α from sin α = a/ρi; span S = 2a;
   - the slice's own intrados rise above its springing on the bearing walls, hi = ρi(1 − cos α).
     That is the dome's height above the springline at that y, less the bearing wall's segment
     height there, so it is much less than f.
3. Per unit length of each bearing wall, with every layer k's weight per radian added up (the
   blanket counts as load):
   - thrust H(y) = Σ γk ts,k rs,k × (α sin α − 1 + cos α)/(1 − cos α), the §D3 formula;
   - vertical V(y) = Σ γk ts,k rs,k × α.
   - For shallow slices the bracket tends to 1, so H ≈ qR, about twice the four-wall average
     H_c ≈ qR/2.
4. Frame: each bearing wall's total thrust T_w = ∫H dy is taken at its ends. A tie or frame
   member across the door head and one across the back wall carry T_w/2 each. The bearing walls'
   buttress members bend between the corner posts.
5. Doors in two opposite walls: the same slices still work. Doors in two adjacent walls: no family
   of parallel slices avoids both doors, so this argument fails.
6. Cold check (Heyman): the geometrical factor of safety (ts/rs)/η_min(α) should be at least 2
   for every slice (§D3).
7. Hot check (HarbisonWalker, applying its sprung-arch rules to each slice). [D10] pp. 15–16,
   Verified:
   - "As the arch rises on heat-up, the line of thrust … shifts downward. As the line of thrust
     approaches a horizontal position in the arch, the horizontal force approaches its maximum
     value."
   - "Without adequate provision for thermal expansion, the relationship between arch thickness
     and rise of the cold arch must be such that the line of thrust does not drop out of the arch
     when it is heated. If it does, the arch will not be stable."
   - Footnote: "Assuming that the absolute lower limit for the rise of the line of thrust is
     1/4 inch (1/48) per foot of span … T should not exceed: (h − S/48)/cosine θ/2."
   - "In some cases, horizontal tie rods are spring loaded or manually adjusted to permit thermal
     expansion of the refractories." (The OCR prints "arc" for "are".)
   - So the hot checks are: ts ≤ (hi − S/48)/cos α; rise per foot d = 12 hi/S within HW's 1 to
     3 in/ft (IFB 2–3, `kiln-hardware.md` §4.4); and heated thrust from HW's Hmax table where T/S
     is 4–10 %. Above 10 % there is no sourced heated thrust.

### D4.2 Worked examples (Derived; same chamber and lining as §D2)

| Case | Slice | ts | α | hi (in/ft) | T/S | ts/rs | η_min | Factor | HW limit on ts | H | V |
|---|---|---|---|---|---|---|---|---|---|---|---|
| f = 8 in, door in a 30 in wall (slices span 30 in) | centre | 3.00 in | 23.05° | 3.06 in (1.22) | 10.0 % | 0.075 | 0.00054 | 140 | 2.64 in: **fails** | 78.8 lb/ft | 32.6 lb/ft |
| | edge (at the door) | 3.36 | 26.33° | 3.51 (1.40) | 11.2 % | 0.095 | 0.00091 | 104 | 3.22: **fails** | 78.1 | 37.2 |
| f = 8 in, door in a 36 in wall (slices span 36 in) | centre | 3.00 | 28.02° | 4.49 (1.50) | 8.3 % | 0.075 | 0.00116 | 65 | 4.24: passes | 77.8 | 39.6 |
| | edge | 3.24 | 30.70° | 4.94 (1.65) | 9.0 % | 0.088 | 0.00167 | 53 | 4.87: passes | 77.1 | 43.4 |
| f = 12 in, door in a 30 in wall | centre | 3.00 | 31.30° | 4.20 (1.68) | 10.0 % | 0.099 | 0.00180 | 55 | 4.19: passes | 58.8 | 33.8 |
| | edge | 3.73 | 41.63° | 5.70 (2.28) | 12.4 % | 0.153 | 0.00553 | 28 | 6.79: passes | 56.4 | 45.0 |
| f = 20 in, door in a 30 in wall | centre | 3.00 | 39.22° | 5.34 (2.14) | 10.0 % | 0.119 | 0.00438 | 27 | 6.09: passes | 47.4 | 35.2 |
| | edge | 4.30 | 76.05° | 11.73 (4.69) | 14.3 % | 0.244 | 0.0566 | 4.3 | passes | 35.9 | 68.3 |

Totals per bearing wall (Derived):

| Case | Thrust | Vertical | Each tie |
|---|---|---|---|
| f = 8 in, door in a 30 in wall | 236 lb | 102 lb | 118 lb |
| f = 8 in, door in a 36 in wall | 194 lb | 102 lb | 97 lb |
| f = 12 in, door in a 30 in wall | 175 lb | 111 lb | 87 lb |
| f = 20 in, door in a 30 in wall | 137 lb | 125 lb | 68 lb |
| Four walls, f = 8 in (§D2), for comparison | 86–103 lb per wall | 49 lb per wall | 43–52 lb |

Smallest rise for which every slice passes the HarbisonWalker limit, 30 × 36 in chamber
**(Derived)**:

| Door in | t = 2 in | t = 3 in | t = 4 in |
|---|---|---|---|
| 30 in wall | 6.45 in | 8.90 in | 11.50 in |
| 36 in wall | 4.60 in | 6.20 in | 7.70 in |

What the examples show (all Derived):
- Cold statics never sets the thickness of these shallow slices. The geometrical factor is 27 to
  140, far above 2. Thickness only starts to matter as the dome nears a hemisphere through the
  corners (f → c), when the slice at the door nears a semicircle (α → 90°, η_min → 0.107); at
  f = 20 in that slice's factor is down to 4.3.
- With a door, the thrust per foot of bearing wall roughly doubles (78 against an average of
  34 lb/ft) and falls on two walls instead of four.
- HarbisonWalker's hot limit is the check that bites, and it runs against thickness: for a flat
  slice, a thicker dome needs more rise. The repo's example (3 in over a 30 in front door, 8 in
  rise) is slightly too thick for its slices' 3.1–3.5 in of own rise. It passes with the door in
  the 36 in wall, or with a rise of 8.9 in or more.
- Most studio slices near the door have T/S above 10 %, outside HW's heated-thrust table. That
  is the same gap as `kiln-hardware.md` §4.6.
- Compressive stress is small: 79 lb/ft on 3 × 12 in is 2.2 psi, against Kast-O-Lite 30's modulus
  of rupture of 300–900 psi (`combustion-and-masonry.md` §6.1). The checks are about geometry and
  thrust, not strength.
- The slices weigh 204 lb in all against the dome's 196 lb. The difference is the material over
  the walls that the radial springing joints take in.

---

## D5. Practice and precedent: ovens and kilns with domes and doors

| Item | Value | Mark | Source |
|---|---|---|---|
| Argentine "half orange" charcoal kiln (a dome with doors in its shell) | "The shape is hemispherical, of a diameter of about 6 m (range 5-7 m)." Bricks 0.24 × 0.12 × 0.06 m in mud and charcoal fines, "usually with no iron or steel support at any place". "The kiln has two doors, diametrically opposite each other … The height of each door is 160-170 m [cm is meant], the width at the bottom is 1.10 m and at the top 0,70 m", bricked up for each burn. Fig. 5: "Shell is mostly a single leaf of bricks with a double layer surrounding each door. Extra brick columns at each side of door are common." About 6,000 bricks. Elsewhere the chapter says these kilns "require no steel except a few bars of flat steel over doors and as reinforcement at the base of the dome in the case of the Brazilian furnace" | Verified | [D11] §7.1.2, Fig. 5 |
| Brazilian beehive charcoal kiln | diameter 5 m. Wall "1 brick", complete at "a height of 1.80 m". Doors "1 m wide and 1.6 to 1.7 m high" in the wall: "place across the door columns, in line with the walls, a steel plate or pieces of bamboo and continue the laying of the bricks of the walls over these"; "Door columns reinforced with one additional brick". "The dome is constructed with the thickness of half a brick", with minimal mortar, "kept in position more by lateral pressure than by mortar". At its base, "a steel ring or several rounds of fencing wire … adjust it without tightening too much. (Final adjustment is made after the dome is complete)". "8,500 burnt clay bricks with only one steel band for dome" | Verified | [D11] §7.2; App. 1 steps 7–8, 16–18, 21 |
| Earth oven (Denzer) | sand form 12–16 in high. "The mud layer should be 3-4 inches thick (no thin spots!)". "Door width should be about half the hearth diameter (10-12 inches)." "Door height should be 63% of the height of your sand form (7.5 - 10 inches)"; "The 10" height of your door opening is a critical 63% of your 16" dome". The door is marked and cut "through the moist mix", so the dome carries itself over it; a brick door arch is optional (index: pp. 36, 45, 48–49). The 63 % comes from *The Bread Ovens of Quebec*. "Rushed ovens can collapse, especially if the dome is a bit flat" | Excerpt | [D12] |
| — check against Heyman (Derived) | 3–4 in of mud over a 20–27 in hearth (Denzer's plans include 22.5, 27 and 36 in) gives a centre-line t/r of about 0.20–0.33, two to three times the semicircular-arch minimum (0.107). By the half-dome argument (§D4), such a dome would stand with half of it cut away, so a door half the diameter wide is well inside that. (This treats the dome as a hemisphere; Denzer's 16 in form over a 27 in hearth is a little taller) | Derived | |
| — half orange, same check (Derived) | a single leaf is 0.12 m or 0.24 m thick depending on how the bricks are laid (not stated), so t/r ≈ 0.04 or 0.08 on a 3 m radius. That is below the semicircular arch's 0.107: this kiln stands as a nearly complete dome with small doors (each about 5 % of the base circle), thickened around each door | Derived | |
| Pompeii (brick) pizza oven | glennb (2009): the entry arch "isn't an issue for the oven entry, as it's braced against the dome anyway". carloswlkr (2009): "a 20" wide opening, with a height in the middle of 12"". Search summaries of other threads: 19 × 12 in suggested for a 42 in oven, 20 × 12.5 in in Forno Bravo's e-book, door height about 63–65 % of the dome's height as a rule of thumb | (secondary); Excerpt for the search summaries | [D19] |
| Forno Bravo Casa2G kit | 2 in cast dome on 32–44 in floors (2014 datasheet). Its commercial ovens "cast … to a minimum of 4″" | Excerpt | [D20] |
| Low (Neapolitan) domes | Mike Stansbury (2017): "the weight of the dome pushes down and outward on the lower wall bricks"; of a banded oven, "the bands did not cross the opening of the oven", with "steel vertical posts embedded in the hearth on either side of the door" (which oven is not clear from the text read; he mentions his own 39 in oven and another builder's bands); "I wouldn't trust just the cap ring as my only buttress for the oven". david s (2019): "Getting a steel band all the way around the dome presents problems because the oven door is in the way. Some builders have overcome this problem by anchoring the band into the supporting slab at the sides of the oven door"; "The band should go where the most thrust will be ie at the top of the soldier course" | (secondary) | [D19] |
| Small cast-dome kiln | david s (2011–2013): 4 ft³, single LPG burner. Walls 35 mm thick, of 50/50 crushed firebrick and castable with stainless needles, cast as a cylinder in three interlocking pieces. "A dome in the same brew will sit on top." Door of three cast pieces placed at each loading. Fired to 1,020 °C | (secondary) | [D19] |
| Domed up-draught kilns (Bourry) | "Two side doors, placed over one another and walled up during the burning"; "vertical supports of wood or iron, fixed at their base in the ground, and joined at the top by iron bands passing over the dome. The shape of the burning chamber may be square, rectangular or circular." Round up-draught kiln: "Circular iron bands, principally put above the fire-holes and on a level with the springing of the dome, help to strengthen the kiln." Rectangular down-draught under a crown: "girders on each side of the fire-holes, joined together by tie-rods above". "Round kilns are easily strengthened by means of iron hoops, tightened by wooden wedges or screws" | Verified | [D14] pp. 210–212, 232 |
| Round down-draught kilns (Searle) | "The walls of a circular down-draught kiln must be of considerable thickness, and must, usually, be surrounded by iron bands in order to prevent it being damaged by expansion." The crown is "part of a true circle though not a complete semi-circle. This form of crown is much stronger and in every way preferable to one which is either more pointed or flatter." Wicket arches are "of a semi-circular or Roman type. The distance r should never be less than 20 in." "Flattened arches are, therefore, to be avoided" | Verified | [D13] pp. 249–250, 316–318 |
| Thick walls instead of steel (Olsen) | "This is why many early kilns with walls 18-22 1/4" thick (in some cases up to 3 to 5 feet) could carry the thrust of the dome without rein-forcing supports" | Excerpt | [D15] |
| Bottle kilns (Rhodes) | round updraft kilns, "necessitating thick wall sections and heavy external bracing of chains or iron bands" | Excerpt | [D16] |
| Bottle oven, Stoke-on-Trent | "a domed roof, the CROWN, and its wall are approximately one foot thick". "Iron bands known as BONTS, set about twelve inches apart, run right round the circular oven". "A doorway, the CLAMMINS or WICKET, surrounded by a stout iron frame", just large enough for a man with a saggar on his head, "blocked up with bricks and sand" after placing | (secondary) | [D18] |
| 1886 patent (Pike & Schopp) | a cylindrical kiln "provided with a domeshaped crown". "The door of the kiln is provided with an arched iron frame". "series of metallic bands, M, which extend around the kiln and bind the walls securely together", "the ends of said bands at the door being bent and fastened over the outer edge of the frame" | Verified | [D17] |
| Castable dome (Olsen) | "Using a castable like Kaolite 2,500 or 2,600 LI is relatively an easy procedure with the most important factor being the proper mixing". A form "shaped with dirt, then capped with wet sand for the final smoothing and shaping" | Excerpt | [D15] p. 31 |
| Circular domed downdraft (Olsen) | Mansimran Singh's coal-fired kiln, New Delhi, "approximately 585 cubic feet". Door details not read | Excerpt | [D15] |
| Thin tile domes (MIT tests) | two domes: embrace 45° and 60°, radii 5.0 and 4.1 ft, t/R 0.021 and 0.025, heights 1.5 and 2.1 ft; the table also gives 1.25 in thickness and a 7.0 ft span (its layout is garbled). "One steel tension ring, fabricated with an inside diameter of 86.8 in. (7.2 ft), was used to resist the outward thrust at the base of both domes"; the tiles sat in gypsum in the ring's angle | Verified | [D3] pp. 101–102 |
| Pines Calyx tile domes | span 38 ft, rise 4.3 ft, radius 43 ft, t 0.33 ft (t/R 0.0076), embrace 26°. "A reinforced concrete ring beams resists the outward thrust at the base of each dome". "The horizontal thrust at the bases of both domes is about 188% of the vertical gravity loads on the domes. The high percentage is due to the shallow geometries of the domes." | Verified | [D3] pp. 93–96 |
| Studio kiln with a sail dome over a rectangular chamber and a door in a wall the dome bears on | — | NOT FOUND | |

---

## D6. A dome's thrust and what holds it

- Cap on a ring: T = qR² sin φ0 cos φ0/(1 + cos φ0) (§D1, Derived; checked against [D2]).
- Sail dome on four walls, membrane state, f ≤ 0.486 c: average thrust per unit wall length
  H_c = qR cos φc/(1 + cos φc), exactly (§D2, Derived). In the example it peaks 6–9 % higher at
  mid-wall. A rectangular frame carries half of each wall's total thrust in each member
  perpendicular to that wall.
- Sail dome with a door (§D4): H(y) ≈ qR per unit length on the two bearing walls; a tie across
  the door head and one across the back wall each carry T_w/2 (Derived). The door jambs are the
  bearing walls' free ends. Pitelka adds a vertical angle beside his door because "the stub-wall
  will often warp or lean outwards" (`kiln-hardware.md` §6.2).
- Heated: HarbisonWalker's Hmax factor for an arch "free to rise", T/S 4–10 %
  (`kiln-hardware.md` §4.3). Slices with T/S above 10 %: **NOT FOUND**. Adjustable or
  spring-loaded tie rods allow expansion [D10]. The Brazilian kiln's base ring is fitted "without
  tightening too much" and adjusted after the dome is complete [D11].
- What holds domes in practice:
  - iron bands at the dome's springing (Bourry), or around round kilns (Searle; bottle-oven bonts);
  - a steel ring or several turns of fencing wire at the dome's base (FAO, Brazilian kiln);
  - massive walls (Olsen; the Pantheon, per Lau);
  - a concrete ring beam (Pines Calyx), or a steel ring angle (Lau's tests);
  - for ovens, bands anchored to posts or the slab beside the door (Forno Bravo forum);
  - for kilns, angle frames with ties (`kiln-hardware.md` §4).
- Steel (Derived): 118 lb in a tie at HarbisonWalker's 12,000 psi needs 0.010 in²; a ⅜-16 rod has
  0.0775 in² (`kiln-hardware.md` §4.3, §4.7.3). As with sprung arches, the cold dome thrust does
  not size the rods. The heated thrust is the unknown.

---

## D7. A rule the engine could enforce (Derived, for review)

1. Geometry as `combustion-and-masonry.md` §6.7. Refuse f ≥ c (as now).
2. **No door or car in a wall the dome bears on** (for example, a door below the springline under
   a lintel or arch, which is itself NOT FOUND for sizing): four-wall state.
   - If f ≤ 0.486 c: the average thrust on every wall is H_c = qR cos φc/(1 + cos φc) per unit
     length, about 1.1 H_c at mid-wall in the example. Frame members carry half the
     perpendicular walls' totals.
   - If f > 0.486 c: the membrane state needs tension, so use the sliced state's thrust (item 3)
     in both directions.
3. **A door in one wall, or doors in two opposite walls, up to the whole wall wide**: the dome
   carries itself as parallel arches spanning the other two walls if all of these hold:
   - (a) those two walls have no door or car along their length;
   - (b) every slice has (ts/rs)/η_min(α) ≥ 2 (Heyman), with η_min from [D5] and the §D3 table;
   - (c) every slice has ts ≤ (hi − S/48)/cos α and 1 ≤ 12 hi/S ≤ 3 in/ft (HarbisonWalker),
     unless the design provides for expansion. In that case HarbisonWalker gives no limit either
     way: say so in the working;
   - (d) the frame takes H(y) along each bearing wall, and T_w/2 in a tie across the door head
     and in one across the back wall. Heated thrust from HarbisonWalker's Hmax table when T/S is
     at most 10 %; otherwise refuse to size steel for the heated case (ADR 0009).
4. **Doors in two adjacent walls**: refuse, unless an arch or lintel carries the dome over one of
   them (sizing NOT FOUND).
5. Working steps cite:
   - Heyman's half-dome slicing ([D4], Excerpt) and the safe theorem ([D3] quoting Heyman, [D7]);
   - η_min ([D5] Verified at 60°, 90°, 120°; Derived elsewhere);
   - the thrust formula (Derived, checked against [D10]'s constants);
   - HarbisonWalker's thickness limit and Hmax table ([D10]). Applying them to dome slices is an
     assumption, recorded as such.
6. Range checked (ADR 0009):
   - η_min was derived for α from 10° to 90°;
   - HarbisonWalker's table covers T/S from 4 % to 10 % and 1 to 3 in/ft;
   - the four-wall membrane state holds for f ≤ 0.486 c.

---

## D8. Gaps (not found)

Rules and precedent:
- A sourced rule, from a kiln or oven maker or a code, for when a dome's own thickness carries it
  over a door in a wall it bears on. §D7 is derived from Heyman's half-dome slicing; no source
  states it for sail domes.
- A studio kiln with a sail dome (or any dome) over a rectangular chamber and a door in a wall
  the dome bears on, with dimensions.
- A maker's table of cast refractory dome thickness against span. Forno Bravo's 2 in and 4 in
  figures are search summaries only; its documents returned 403.
- *The Bread Ovens of Quebec* (Boily and Blanchette) itself. The 63 % door rule is known only
  through Denzer.

Theory:
- Membrane or thrust-line solutions for sail vaults (domical vaults) on four walls in a published
  source. §D2's distribution is derived. The Italian literature on sail vaults (Barsi, Barsotti
  and Bennati; Angelillo) was found but not read (paywalled).
- Heyman's Fig. 3.13 values (minimum thickness of incomplete domes) and his figure for the half
  dome's thickness. Only the text around them was readable.
- Whether HarbisonWalker's thickness limit and Hmax table, written for brick sprung arches, apply
  to slices of a cast dome. §D4 assumes they do.
- The friction or bond needed at the wall tops to carry the dome's shear near the corners. §D2
  gives the shear, not the capacity.

Thrust and steel:
- The heated (thermal) thrust of domes, and of arches with T/S above 10 % (same gap as
  `kiln-hardware.md` §4.6).
- Sizing a door arch or lintel under a dome. The wall above a door below the springline carries
  the dome's vertical load and is pushed outward by its thrust.
- Band or ring sizes (section, spacing, tension) for domed kilns. Sources say only "iron bands",
  "one steel band", "a steel ring or several rounds of fencing wire", or bonts "about twelve
  inches apart".

---

## Sources

- [D1] S. Timoshenko, *Theory of Plates and Shells*, 1st ed., McGraw-Hill, 1940, pp. 359–360, eq. (211) (Digital Library of India scan). https://archive.org/details/in.ernet.dli.2015.133398 . Formulas and §111 read in the 2nd ed. (S. Timoshenko and S. Woinowsky-Krieger, 1959): §106 pp. 436–437, eq. (257); §111 "Spherical Shell Supported at Isolated Points", pp. 453–457. Read in an Internet Archive user upload, https://archive.org/details/TheoryOfPlatesAndShells ; library record (borrow-only) https://archive.org/details/theoryofplatessh0000timo
- [D2] Budapest University of Technology and Economics, *Solution Manual: Mechanics of Civil Engineering Structures*, Problem 11.2 "Spherical dome" (eqs. 11-32, 11-33, 11-35). https://solutionmanual.bme.hu/?p=5397
- [D3] W. W. Lau, *Equilibrium Analysis of Masonry Domes*, S.M. thesis, MIT, 2006. http://web.mit.edu/masonry/papers/wwLau_SMBT_2006.pdf ; record https://dspace.mit.edu/handle/1721.1/34984
- [D4] J. Heyman, *The Stone Skeleton: Structural Engineering of Masonry Architecture*, Cambridge University Press, 1995. Borrow-only scan, read through full-text search: https://archive.org/details/stoneskeletonstr0000heym . Chapter pages (summaries): Ch. 2 https://www.cambridge.org/core/books/abs/stone-skeleton/structural-theory-of-masonry/2DF738498EAAF6BEA2B58C9DA6388DFF ; Ch. 3 https://www.cambridge.org/core/books/stone-skeleton/domes/B104A6FD740B6A24FDE62A7B0CA4ED2C
- [D5] E. Rizzi, G. Cocchetti, G. Colasante, F. Rusconi, "Analytical and Numerical Analysis on the Collapse Mode of Circular Masonry Arches", SAHC 2010, *Advanced Materials Research* 133–134, pp. 467–472. https://dinamico2.unibg.it/erizzi/CV/PaperSAHC10RizzietalFinal.pdf
- [D6] T. Ther, I. Sajtos, M. Armuth, L. Strommer, "Ribbed vaults of the Nagyvázsony monastery church – Geometrical factor of safety highlights the secret", *Periodica Polytechnica Architecture* 41/1 (2010), pp. 3–8. https://pp.bme.hu/ar/article/download/6/6
- [D7] P. Block, J. Ochsendorf, "Thrust Network Analysis: A new methodology for three-dimensional equilibrium", *Journal of the IASS* 48(3), 2007. http://web.mit.edu/masonry/papers/block_ochs_IASS_2007.pdf
- [D8] G. Tempesta, M. Paradiso, S. Galassi, E. Pieroni, "Maurice Lévy's original contribution to the analysis of masonry domes", *Domes and Cupolas* 2(2), 2015, p. 85 ff. https://flore.unifi.it/retrieve/e398c37a-5f50-179a-e053-3705fe0a4cff/Maurice%20L%c3%a9vy%e2%80%99s%20original%20contribution%20to%20the%20analysis%20of%20masonry%20domes.pdf
- [D9] N. A. Nodargi, P. Bisegna, "Collapse capacity of masonry domes under horizontal loads: A static limit analysis approach", arXiv:2106.12982, 2021. https://arxiv.org/abs/2106.12982 ; and "Minimum thrust and minimum thickness of spherical masonry domes: a semi-analytical approach", *European Journal of Mechanics A/Solids* 87 (2021) 104222 (repository abstract). https://art.torvergata.it/handle/2108/265855
- [D10] Harbison-Walker Refractories, *Brick Installation Guide*, 2008, pp. 12, 15–16, 18, 28 (= [S20] in `kiln-hardware.md`). https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf . Also *Modern Refractory Practice*, 1950, searched through full text: https://archive.org/details/modernrefractory00harb
- [D11] FAO, *Simple technologies for charcoal making*, FAO Forestry Paper 41, Ch. 7 "Brick kilns" (§7.1 half-orange Argentine kiln, §7.2 Brazilian beehive kiln): https://www.fao.org/4/x5328e/x5328e08.htm ; Appendix 1, "Building and Operating the Brazilian Beehive Kiln" (extract from L. Osse, *Leña, Carbón y Carbonización*, Salta, 1974): https://www.fao.org/4/X5328e/x5328e0g.htm
- [D12] K. Denzer, *Build Your Own Earth Oven*, Hand Print Press, 2007. Borrow-only, read through full-text search. https://archive.org/details/buildyourowneart0000denz_x3k5
- [D13] A. B. Searle, *Modern Brickmaking*, Scott, Greenwood & Son, London, 1911, pp. 249–250, 316–318. https://archive.org/details/modernbrickmakin00searrich
- [D14] E. Bourry, *A Treatise on Ceramic Industries*, translated by A. B. Searle, Scott, Greenwood & Son, London, 1911, pp. 210–212, 231–232. https://archive.org/details/treatiseoncerami00bouriala
- [D15] F. L. Olsen, *The Kiln Book*, 3rd ed., Krause, 2001. Borrow-only, read through full-text search. https://archive.org/details/kilnbook00fred
- [D16] D. Rhodes, *Kilns: Design, Construction, and Operation*, Chilton, 1968 (= [S34] in `kiln-hardware.md`), read through full-text search. https://archive.org/details/kilnsdesignconst00rhod
- [D17] E. M. Pike, J. B. Schopp, US Patent 340,003, "Tile and pottery kiln", 1886-04-13. https://patents.google.com/patent/US340003A/en
- [D18] thepotteries.org, "How the Bottle Kiln works". https://www.thepotteries.org/bottle_kiln/bottle_kiln_two.htm (secondary)
- [D19] Forno Bravo forum: "Oven opening: arch vs straight sides" (2009), https://community.fornobravo.com/forum/good-background-information/newbie-forum/6037-oven-opening-arch-vs-straight-sides ; "Low dome build" (2017), https://community.fornobravo.com/forum/pizza-oven-design-and-installation/pompeii-oven-construction/400609-low-dome-build ; "My Neapolitan style oven in progress" (2019), https://community.fornobravo.com/forum/good-background-information/brick-oven-photos/414160-my-neapolitan-style-oven-in-progress ; "Pizza oven becomes a kiln" (2011–2013), https://community.fornobravo.com/forum/pizza-oven-design-and-installation/other-oven-types/14564-pizza-oven-becomes-a-kiln (all secondary)
- [D20] Forno Bravo, Casa2G datasheet, https://www.fornobravo.com/newsletters/graphics/Jul13/Casa2G_datasheet.pdf and https://fornobravo.com/PDF/Casa2G_datasheet.pdf ; "Optimal dome thickness", https://www.fornobravo.com/commercial-pizza-ovens/compare/optimal-dome-thickness/ (403 to direct fetch; search summaries only)
- [D21] M. Fantin, T. Ciblac, M. Brocato, "Resistance of flat vaults taking their stereotomy into account", *Journal of Mechanics of Materials and Structures* 13(5), 2018, p. 657 ff. https://msp.org/jomms/2018/13-5/jomms-v13-n5-p06-p.pdf
- [D22] C. Cusano, C. Cennamo, M. Angelillo, "Seismic vulnerability of domes: a case study", *Journal of Mechanics of Materials and Structures* 13(5), 2018, p. 679 ff. https://msp.org/jomms/2018/13-5/jomms-v13-n5-p07-p.pdf
- [D23] W. Trinks, *Industrial Furnaces*, 1925, 1926 and 1951 (Vol. I) editions, searched for domes with none found. https://archive.org/details/industrialfurnac0000wtri ; https://archive.org/details/industrialfurnac0002trin ; https://archive.org/details/dli.ernet.17458
