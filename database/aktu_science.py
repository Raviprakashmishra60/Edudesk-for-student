"""Basic Science subjects: Engineering Physics, Engineering Chemistry, Engineering Mathematics-I and II."""
from database.aktu_content import SUBJECT, U

# ====================================================================== PHYSICS
PHYSICS = SUBJECT(
    "BAS101", "BAS201", "Engineering Physics", "Basic Science", 4, "3-1-0",
    "Understand quantum mechanics, electromagnetic theory, wave optics, fibre optics and lasers, and superconductors and nano-materials, and apply them to engineering problems.",
    ["Concepts of Modern Physics - Arthur Beiser (McGraw-Hill)", "Optics - Brijlal & Subramanian (S. Chand)",
     "Engineering Physics: Theory and Practical - Katiyar & Pandey (Wiley India)", "Applied Physics for Engineers - Neeraj Mehta (PHI Learning)",
     "Engineering Physics - Malik H.K. & Singh A.K. (McGraw-Hill)"],
    [
        U(1, "Quantum Mechanics", 9,
          "Inadequacy of classical mechanics, Planck's theory of black body radiation (qualitative), Compton effect, de-Broglie concept of matter waves, Davisson and Germer experiment, phase velocity and group velocity, time-dependent and time-independent Schrodinger wave equations, physical interpretation of wave function, particle in a one-dimensional box.",
          [("Black body radiation and Planck's idea", [
              "A black body absorbs all radiation falling on it and emits a characteristic spectrum depending only on temperature.",
              "Classical (Rayleigh-Jeans) theory fits long wavelengths but predicts infinite energy at short wavelengths - the 'ultraviolet catastrophe'. Wien's law fits only short wavelengths.",
              "Planck's quantum hypothesis: energy is emitted or absorbed in packets (quanta) E = hv, so total energy is n·hv (n = 0, 1, 2 ...). h = 6.626 x 10^-34 J·s.",
              "Wien's displacement law: λmax · T = 2.898 x 10^-3 m·K (peak wavelength shifts to shorter values as T rises)."]),
           ("Compton effect", [
              "When X-rays scatter from a (nearly) free electron, the scattered X-ray has a longer wavelength than the incident one.",
              "Compton shift: Δλ = λ' - λ = (h / m0·c)(1 - cos θ). The quantity h/m0c = 0.0243 Å is the Compton wavelength.",
              "Shift is zero at θ = 0° and maximum (2h/m0c) at θ = 180°; it does not depend on the incident wavelength or the scatterer.",
              "Explained by treating a photon as a particle colliding with an electron (conservation of energy and momentum). It proves the particle nature of radiation."]),
           ("de Broglie matter waves", [
              "Every moving particle has an associated wave: λ = h/p = h/mv.",
              "Electron accelerated through potential V volts: λ = 12.27/√V Å. For a particle of kinetic energy E: λ = h/√(2mE).",
              "Matter waves are not electromagnetic waves; they are probability waves. Wave nature of macroscopic objects is unobservable because λ is extremely small."]),
           ("Davisson-Germer experiment", [
              "Electrons from a heated filament are accelerated through 54 V and strike a nickel crystal; a detector measures electrons scattered at different angles.",
              "A sharp maximum appears at a scattering angle of 50° - a diffraction pattern, which proves the wave nature of electrons.",
              "Using nλ = d sin φ with the nickel lattice spacing d = 2.15 Å gives λ ≈ 1.65 Å, in close agreement with de Broglie's 12.27/√54 ≈ 1.67 Å."]),
           ("Phase velocity and group velocity", [
              "Phase velocity vp = ω/k = velocity of a single wave crest. For matter waves vp = c²/v which is greater than c (no energy travels at vp).",
              "Group velocity vg = dω/dk = velocity of the wave packet = particle velocity v.",
              "Relation: vp · vg = c²."]),
           ("Schrodinger equations and the wave function", [
              "Time-dependent: iħ ∂ψ/∂t = -(ħ²/2m) ∇²ψ + Vψ, where ħ = h/2π.",
              "Time-independent (steady state): ∇²ψ + (2m/ħ²)(E - V)ψ = 0. In 1-D: d²ψ/dx² + (2m/ħ²)(E - V)ψ = 0.",
              "Wave function ψ has no direct meaning; |ψ|² is the probability density, and ∫|ψ|² dτ = 1 (normalisation).",
              "Acceptable ψ must be single-valued, finite, continuous (with continuous first derivative) and normalisable."]),
           ("Particle in a one-dimensional box (infinite well)", [
              "Potential V = 0 for 0 < x < L and V = ∞ outside, so ψ = 0 at x = 0 and x = L.",
              "Solution: ψn(x) = √(2/L) sin(nπx/L), n = 1, 2, 3 ...",
              "Energy: En = n²h²/(8mL²). Energy is quantised; the lowest energy E1 = h²/(8mL²) is not zero (zero-point energy).",
              "Level spacing grows as n²; ψn has (n - 1) nodes; probability density is not uniform inside the box."])],
          ["S: State Planck's quantum hypothesis.", "S: What is the Compton wavelength? Give its value.",
           "S: Write the de Broglie wavelength of an electron accelerated through V volts.", "S: Why can the wave nature of a cricket ball not be observed?",
           "S: State the physical significance of the wave function.", "S: What are the conditions for a well-behaved wave function?",
           "S: Define phase velocity and group velocity and state the relation between them.",
           "L: Explain the Compton effect and derive the expression for the Compton shift.",
           "L: Describe the Davisson-Germer experiment and show how it verifies de Broglie's hypothesis.",
           "L: Derive the time-independent Schrodinger equation.",
           "L: Find the eigenvalues and normalised eigenfunctions of a particle in a one-dimensional box of width L.",
           "N: Calculate the de Broglie wavelength of an electron accelerated through 100 V.",
           "N: X-rays of wavelength 1 Å are scattered at 90° by a free electron. Find the wavelength of scattered X-rays.",
           "N: An electron is confined in a 1-D box of width 1 Å. Find its lowest two energy levels in eV."]),

        U(2, "Electromagnetic Field Theory", 8,
          "Basic concept of Stoke's theorem and Divergence theorem, basic laws of electricity and magnetism, continuity equation for current density, displacement current, Maxwell equations in integral and differential form, Maxwell equations in vacuum and in conducting medium, Poynting vector and Poynting theorem, plane electromagnetic waves in vacuum and their transverse nature, relation between electric and magnetic fields of an electromagnetic wave, plane electromagnetic waves in conducting medium, skin depth.",
          [("Vector theorems", [
              "Divergence (Gauss) theorem: ∮ A·dS = ∭ (∇·A) dV - converts a closed-surface integral to a volume integral.",
              "Stokes' theorem: ∮ A·dl = ∬ (∇×A)·dS - converts a closed-loop integral to a surface integral."]),
           ("Basic laws", [
              "Gauss's law (electric): ∮ D·dS = q. Gauss's law (magnetic): ∮ B·dS = 0 (no magnetic monopoles).",
              "Faraday's law: emf = -dΦB/dt. Ampere's circuital law: ∮ H·dl = I."]),
           ("Continuity equation and displacement current", [
              "Conservation of charge: ∇·J + ∂ρ/∂t = 0.",
              "Ampere's law ∇×H = J fails for a charging capacitor (take divergence: ∇·J would have to be 0). Maxwell added the displacement current density Jd = ∂D/∂t.",
              "Modified law: ∇×H = J + ∂D/∂t. Displacement current Id = ε0 dΦE/dt exists in vacuum/dielectric where no charge flows."]),
           ("Maxwell's equations", [
              "Differential form: ∇·D = ρ; ∇·B = 0; ∇×E = -∂B/∂t; ∇×H = J + ∂D/∂t.",
              "Integral form: ∮D·dS = q; ∮B·dS = 0; ∮E·dl = -dΦB/dt; ∮H·dl = I + dΦD/dt.",
              "Vacuum (ρ = 0, J = 0): ∇·E = 0; ∇·B = 0; ∇×E = -∂B/∂t; ∇×B = μ0ε0 ∂E/∂t.",
              "Conducting medium (J = σE; free charge decays quickly so ρ ≈ 0): ∇×H = σE + ε ∂E/∂t."]),
           ("Poynting vector and theorem", [
              "Poynting vector S = E × H (unit W/m²) gives the rate of energy flow per unit area, in the direction of wave propagation.",
              "Poynting theorem (energy conservation): -∮ (E×H)·dS = ∂/∂t ∭ (½εE² + ½μH²) dV + ∭ J·E dV. Power flowing in = rate of increase of stored field energy + ohmic loss."]),
           ("Plane EM waves in vacuum", [
              "Wave equation: ∇²E = μ0ε0 ∂²E/∂t². Speed c = 1/√(μ0ε0) = 3 x 10^8 m/s.",
              "E, B and the direction of propagation are mutually perpendicular - the wave is transverse. E/B = c and E, B are in phase.",
              "Intensity I = ½ ε0 c E0²."]),
           ("Plane EM waves in a conducting medium and skin depth", [
              "Equation: ∇²E = μσ ∂E/∂t + με ∂²E/∂t². The conduction term makes the wave decay as it travels: E = E0 e^(-z/δ) cos(ωt - kz).",
              "Skin depth δ = √(2/(ωμσ)) = 1/√(π f μ σ) - the depth at which the amplitude falls to 1/e (about 37%).",
              "Skin depth is small at high frequency, so high-frequency current flows near the surface of a conductor (skin effect)."])],
          ["S: State Stokes' theorem and the divergence theorem.", "S: Write the continuity equation for current density.",
           "S: What is displacement current? Write its expression.", "S: Write Maxwell's four equations in differential form.",
           "S: What is the Poynting vector? State its unit.", "S: Define skin depth.", "S: Why are electromagnetic waves called transverse?",
           "L: Derive Maxwell's equations in differential form and explain the need for displacement current.",
           "L: State and prove Poynting theorem.",
           "L: Derive the wave equation for EM waves in free space and show that they are transverse with E/B = c.",
           "L: Derive the wave equation in a conducting medium and obtain the expression for skin depth.",
           "N: Find the displacement current in a parallel-plate capacitor of area 0.02 m² when the electric field changes at 10^12 V/m·s.",
           "N: Calculate the skin depth of copper (σ = 5.8 x 10^7 S/m, μ = μ0) at 1 MHz.",
           "N: The electric field amplitude of a plane EM wave in vacuum is 100 V/m. Find the magnetic field amplitude and the average intensity."]),

        U(3, "Wave Optics", 10,
          "Coherent sources, interference in uniform and wedge shaped thin films, necessity of extended sources, Newton's rings and its applications, introduction to diffraction, Fraunhoffer diffraction at single slit and double slit, absent spectra, diffraction grating, spectra with grating, dispersive power, resolving power, Rayleigh's criterion of resolution, resolving power of grating.",
          [("Coherent sources and thin-film interference", [
              "Coherent sources have a constant phase difference and same frequency; they are produced by division of wavefront or amplitude.",
              "Extended source: a point source shows fringes only near its position; an extended source lets the whole film be seen with bright fringes at all positions.",
              "Reflected light from a uniform film (thickness t, refractive index μ, refraction angle r): path difference = 2μt cos r + λ/2 (extra λ/2 from reflection at the denser surface).",
              "Constructive (bright): 2μt cos r = (2n + 1)λ/2. Destructive (dark): 2μt cos r = nλ. For transmitted light the conditions are interchanged."]),
           ("Wedge-shaped film", [
              "Parallel, equally spaced straight fringes are formed. Fringe width β = λ/(2μθ), where θ is the wedge angle.",
              "Fringes are fewer and wider for a small angle; the edge in contact appears dark in reflected light."]),
           ("Newton's rings", [
              "A plano-convex lens of large radius R placed on a flat glass plate gives an air film of increasing thickness - concentric circular fringes in reflected light with a dark centre.",
              "Dark rings: Dn² = 4nλR. Bright rings: Dn² = 2(2n - 1)λR. Diameters are proportional to √n.",
              "Wavelength: λ = (D²(n+m) - D²n)/(4mR). Refractive index of a liquid: μ = (D²(n+m) - D²n)air / (D²(n+m) - D²n)liquid.",
              "Applications: finding wavelength of light, refractive index of a liquid, testing flatness of surfaces and radius of curvature of lenses."]),
           ("Diffraction and single slit", [
              "Diffraction: bending of light around obstacles of size comparable to the wavelength. Fraunhofer (parallel waves, far field) is studied here.",
              "Single slit of width a: intensity I = I0 (sin α/α)², α = (πa sin θ)/λ.",
              "Minima: a sin θ = nλ (n = ±1, ±2 ...). Central maximum is brightest and twice as wide as other maxima; secondary maxima are weak."]),
           ("Double slit and absent spectra", [
              "Pattern = single-slit diffraction envelope x two-slit interference. Interference maxima: (a + b) sin θ = nλ; diffraction minima: a sin θ = mλ.",
              "When both conditions are satisfied together, the interference order n is missing (absent spectrum): n = m(a + b)/a. If a + b = 2a, orders 2, 4, 6 ... are absent."]),
           ("Diffraction grating", [
              "A grating has a large number of equally spaced parallel slits; grating element (a + b) = 1/N per cm.",
              "Principal maxima: (a + b) sin θ = nλ. Maximum possible order n < (a + b)/λ. With white light each order (except zero) gives a spectrum.",
              "Dispersive power: dθ/dλ = n/((a + b) cos θ). Higher order and smaller grating element give greater dispersion."]),
           ("Resolving power", [
              "Rayleigh's criterion: two spectral lines are just resolved when the central maximum of one falls on the first minimum of the other.",
              "Resolving power R = λ/dλ. For a grating R = nN (order x total number of lines). For a prism R = t(dμ/dλ)."])],
          ["S: What are coherent sources? How are they obtained?", "S: Why is an extended source necessary to see thin-film fringes?",
           "S: Why is the centre of Newton's rings dark in reflected light?", "S: What is meant by absent spectra?",
           "S: State Rayleigh's criterion of resolution.", "S: Define dispersive power and resolving power of a grating.",
           "L: Derive the conditions of bright and dark fringes for reflected light from a thin parallel film.",
           "L: Explain the formation of Newton's rings and derive expressions for the diameters of dark rings. How is the wavelength of light determined?",
           "L: Discuss Fraunhofer diffraction at a single slit and obtain the intensity distribution.",
           "L: Explain Fraunhofer diffraction at a double slit and discuss absent spectra.",
           "L: Describe the diffraction grating and derive the expressions for dispersive power and resolving power.",
           "N: In Newton's rings, the diameters of the 5th and 15th dark rings are 0.336 cm and 0.590 cm. Find the radius of curvature of the lens if λ = 5890 Å.",
           "N: A grating has 6000 lines per cm. Find the maximum order visible with λ = 5000 Å and the angular position of the first order.",
           "N: Find the minimum number of lines in a grating needed to resolve the sodium D lines (5890 Å and 5896 Å) in the first order."]),

        U(4, "Fiber Optics & Laser", 9,
          "Fibre optics: principle and construction of optical fiber, acceptance angle, numerical aperture, acceptance cone, step index and graded index fibers, fiber optic communication principle, attenuation, dispersion, application of fiber. Laser: absorption of radiation, spontaneous and stimulated emission of radiation, population inversion, Einstein's coefficients, principles of laser action, solid state laser (Ruby laser) and gas laser (He-Ne laser), laser applications.",
          [("Optical fibre - principle and construction", [
              "Principle: total internal reflection (TIR). Core refractive index n1 is greater than cladding index n2; a protective buffer/jacket surrounds them.",
              "TIR happens when the angle of incidence at the core-cladding boundary exceeds the critical angle θc = sin⁻¹(n2/n1)."]),
           ("Acceptance angle and numerical aperture", [
              "Acceptance angle θ0: maximum angle at the fibre end for which light is still guided: n0 sin θ0 = √(n1² - n2²). For air n0 = 1.",
              "Numerical aperture NA = sin θ0 = √(n1² - n2²) = n1√(2Δ), with relative index difference Δ = (n1 - n2)/n1.",
              "Acceptance cone: cone of full angle 2θ0 around the fibre axis; light inside it is guided. Larger NA means more light gathering."]),
           ("Types of fibres", [
              "Step-index: constant core index with abrupt drop at the cladding; single-mode (core ~ 8-10 µm) and multimode.",
              "Graded-index: core index decreases gradually from centre to cladding; rays follow curved paths, giving less intermodal dispersion.",
              "Single-mode step index: lowest dispersion, long distance. Multimode graded index: moderate cost, short-medium distance."]),
           ("Fibre-optic communication, attenuation and dispersion", [
              "Principle: electrical signal → light source (LED/laser diode) → modulated light in fibre → photodetector → electrical signal, with repeaters/amplifiers for long links.",
              "Attenuation (loss): α = (10/L) log10(Pin/Pout) dB/km. Causes: absorption, scattering (Rayleigh), bending losses, connectors.",
              "Dispersion: pulse broadening. Intermodal (different modes), intramodal - material and waveguide dispersion.",
              "Applications: telecom and internet, cable TV, medical endoscopy, sensors, military links, industrial imaging. Advantages: high bandwidth, low loss, immunity to EM interference, light weight."]),
           ("Absorption, spontaneous and stimulated emission", [
              "Absorption: an atom in E1 absorbs a photon hv = E2 - E1 and goes to E2. Rate = B12 N1 ρ(v).",
              "Spontaneous emission: excited atom drops on its own, random phase and direction. Rate = A21 N2.",
              "Stimulated emission: an incoming photon of energy hv triggers emission of an identical photon (same phase, direction, frequency). Rate = B21 N2 ρ(v). It is the basis of laser light."]),
           ("Population inversion and Einstein coefficients", [
              "Normally N1 > N2 (Boltzmann). Population inversion means N2 > N1 for a pair of levels; it is created by pumping and needs metastable states.",
              "At equilibrium: A21 N2 + B21 N2 ρ = B12 N1 ρ. Using Planck's law gives B12 = B21 and A21/B21 = 8πhv³/c³.",
              "Ratio of spontaneous to stimulated emission: A21/(B21 ρ) = e^(hv/kT) - 1 - large at optical frequencies, so inversion is needed for laser action."]),
           ("Laser action, Ruby laser, He-Ne laser", [
              "Laser parts: active medium, pumping source, optical resonator (two mirrors, one partially transparent). Light is amplified by repeated stimulated emission.",
              "Ruby laser: three-level, solid-state; rod of Al2O3 doped with ~0.05% Cr³⁺, pumped by a xenon flash lamp; emits pulsed red light at 6943 Å. Inefficient; needs high pumping.",
              "He-Ne laser: four-level gas laser; mixture He:Ne ≈ 10:1 at low pressure, excited by electric discharge. He atoms are excited and transfer energy to Ne by collisions; emits continuous red light at 6328 Å. Low power, high coherence and stability.",
              "Properties: high directionality, monochromaticity, coherence, intensity. Uses: surgery, welding, cutting, barcode scanners, holography, optical communication, range-finding, CD/DVD readers."])],
          ["S: What is total internal reflection? Give its conditions.", "S: Define acceptance angle and numerical aperture.",
           "S: Distinguish between step-index and graded-index fibres.", "S: What is attenuation in a fibre? Write its formula.",
           "S: Differentiate spontaneous and stimulated emission.", "S: What is population inversion?", "S: Write any four properties of laser light.",
           "L: Derive an expression for the numerical aperture and acceptance angle of a step-index fibre.",
           "L: Explain the types of optical fibres with ray diagrams and refractive index profiles.",
           "L: Explain attenuation and dispersion in optical fibres and list applications of fibres.",
           "L: Derive the relations between Einstein's A and B coefficients.",
           "L: With energy level diagrams describe the construction and working of a Ruby laser.",
           "L: Describe the construction and working of a He-Ne laser.",
           "N: A fibre has core index 1.50 and cladding index 1.45. Find NA, acceptance angle and critical angle.",
           "N: Light of power 5 mW enters a 4 km fibre and 1 mW comes out. Find the attenuation in dB/km."]),

        U(5, "Superconductors and Nano-Materials", 8,
          "Superconductors: temperature dependence of resistivity in superconducting materials, Meissner effect, temperature dependence of critical field, persistent current, Type I and Type II superconductors, high temperature superconductors, properties and applications of superconductors. Nano-materials: introduction and properties of nano materials, basic concept of quantum dots, quantum wires and quantum well, fabrication of nano materials - top-down approach (CVD) and bottom-up approach (Sol Gel), properties and application of nano materials.",
          [("Superconductivity basics", [
              "Below a critical temperature Tc, certain materials show zero electrical resistance (Onnes, 1911, mercury at 4.2 K). Resistivity drops sharply at Tc.",
              "Critical field: a strong enough magnetic field destroys superconductivity: Hc(T) = Hc(0)[1 - (T/Tc)²]; Hc = 0 at T = Tc.",
              "Persistent current: a current induced in a superconducting ring continues for years without decay because resistance is zero."]),
           ("Meissner effect", [
              "A superconductor expels magnetic field from its interior when cooled below Tc (B = 0 inside) - perfect diamagnetism (χ = -1).",
              "This is different from a perfect conductor, which would only freeze the field already present. Meissner effect explains magnetic levitation."]),
           ("Type I and Type II superconductors", [
              "Type I (soft): one critical field Hc, abrupt transition to normal state, complete Meissner effect; low Hc. Examples: Pb, Hg, Sn, Al.",
              "Type II (hard): two critical fields Hc1 and Hc2. Between them is a mixed (vortex) state; superconductivity survives to high fields. Examples: Nb3Sn, NbTi, YBCO.",
              "Type II materials are used in strong magnets because of their large Hc2."]),
           ("High-temperature superconductors, properties and applications", [
              "Ceramic cuprates such as YBa2Cu3O7 (YBCO) have Tc ≈ 90 K, above liquid-nitrogen temperature (77 K) - cheaper cooling.",
              "Properties: zero resistance, Meissner effect, flux quantisation, Josephson effect, energy gap.",
              "Applications: MRI magnets, maglev trains, SQUID magnetometers, lossless power cables, fault-current limiters, particle accelerators, fast electronics."]),
           ("Nanomaterials - introduction and properties", [
              "Nanomaterials have at least one dimension in 1-100 nm. Very large surface-to-volume ratio.",
              "Properties change with size: optical (colour shift), electrical, magnetic, mechanical (stronger), and melting point/chemical reactivity.",
              "Cause: quantum confinement of electrons and the surface effect."]),
           ("Quantum well, wire and dot", [
              "Quantum well: confined in one direction, free in two (2-D). Quantum wire: confined in two directions, free in one (1-D). Quantum dot: confined in all three directions (0-D); discrete atom-like energy levels.",
              "Density of states changes with dimension; dots are tunable by size (used in displays, LEDs, solar cells, bio-imaging)."]),
           ("Fabrication of nanomaterials", [
              "Top-down: bulk material broken or etched into nanoscale (ball milling, lithography). As per AKTU syllabus, CVD is listed under the top-down approach; many textbooks classify CVD as bottom-up - write it as your textbook/teacher expects.",
              "CVD: volatile precursor gas decomposes/reacts on a heated substrate in a chamber and deposits a thin solid film or nanostructure (used for carbon nanotubes, graphene, thin films).",
              "Bottom-up: build from atoms/molecules. Sol-gel: metal alkoxide precursor → hydrolysis and condensation → sol → gel → ageing/drying → calcination → nanopowder.",
              "Applications: medicine (drug delivery), electronics, catalysis, sensors, energy storage, coatings, cosmetics, water purification."])],
          ["S: What is the Meissner effect?", "S: Define critical temperature and critical magnetic field.", "S: What is persistent current?",
           "S: Differentiate Type I and Type II superconductors.", "S: Why are nanomaterials different from bulk materials?",
           "S: Distinguish between quantum well, quantum wire and quantum dot.", "S: Write any four applications of superconductors.",
           "L: Explain the Meissner effect and the temperature dependence of the critical field.",
           "L: Discuss Type I and Type II superconductors with magnetisation curves.",
           "L: Write a note on high-temperature superconductors and their applications.",
           "L: Explain the properties and applications of nanomaterials.",
           "L: Describe the top-down and bottom-up methods of nanomaterial fabrication with CVD and sol-gel as examples.",
           "N: The critical field of lead at 0 K is 6.5 x 10^4 A/m and Tc = 7.2 K. Find the critical field at 5 K."]),
    ],
    labs=[{"code": "BAS151 / BAS251", "title": "Engineering Physics Lab (any ten experiments, at least four from each group)", "items": [
        "Group A: Wavelength of sodium light by Newton's rings", "Group A: Wavelengths of mercury lines using plane transmission grating",
        "Group A: Specific rotation of cane sugar using polarimeter", "Group A: Focal length of a combination of two lenses",
        "Group A: Attenuation in an optical fibre", "Group A: Wavelength of He-Ne laser using single slit diffraction",
        "Group A: Polarization of light using He-Ne laser", "Group A: Wavelength of sodium light using Fresnel's bi-prism",
        "Group A: Coefficient of viscosity of a liquid", "Group A: Acceleration due to gravity using compound pendulum",
        "Group B: Energy band gap of a semiconductor", "Group B: Hall effect - Hall coefficient, carrier density and mobility",
        "Group B: Variation of magnetic field along the axis of a current-carrying coil", "Group B: Verification of Stefan's law",
        "Group B: Specific resistance using Carey Foster's bridge", "Group B: Resonance of a series LCR circuit",
        "Group B: Electrochemical equivalent of copper", "Group B: Calibration of ammeter and voltmeter by potentiometer",
        "Group B: B-H curve and hysteresis loss of a transformer core", "Group B: Measurement of high resistance by leakage method"]}],
)

# ====================================================================== CHEMISTRY
CHEMISTRY = SUBJECT(
    "BAS102", "BAS202", "Engineering Chemistry", "Basic Science", 4, "3-1-0",
    "Understand molecular structure, advanced materials, green chemistry, spectroscopy, stereochemistry, electrochemistry, corrosion, water technology, fuels and polymers for engineering applications.",
    ["Engineering Chemistry - Rath & Singh (Cengage)", "Engineering Chemistry - S.S. Dara (S. Chand)", "Engineering Chemistry - Jain & Jain (S. Chand)",
     "Engineering Chemistry - K. Sesha Maheswaramma (Pearson)", "Engineering Chemistry - O.G. Palanna (McGraw-Hill)",
     "Engineering Chemistry - Shashi Chawla (Dhanpat Rai)", "University Chemistry - B.H. Mahan", "University Chemistry - C.N.R. Rao"],
    [
        U(1, "Atomic and Molecular Structure, Advanced Materials and Green Chemistry", 8,
          "Atomic and molecular structure: molecular orbitals of diatomic molecules, bond order, magnetic characters and numerical problems. Chemistry of advanced materials: liquid crystals (introduction, types, applications, industrially important materials), graphite and fullerene (introduction, structure, applications), nanomaterials (introduction, preparation, characteristics, applications, carbon nanotubes). Green chemistry: introduction, 12 principles and importance of green synthesis, green chemicals, synthesis of adipic acid and paracetamol by conventional and green routes, environmental impact.",
          [("Molecular orbital theory (MOT)", [
              "Atomic orbitals combine (LCAO) to form bonding MOs (lower energy, in-phase) and antibonding MOs (higher energy, out-of-phase). Electrons fill by Aufbau, Pauli and Hund rules.",
              "Bond order = (Nb - Na)/2, where Nb = electrons in bonding MOs, Na = electrons in antibonding MOs. Higher bond order → shorter, stronger bond. BO = 0 means the molecule does not exist.",
              "Magnetic character: all electrons paired → diamagnetic; one or more unpaired → paramagnetic."]),
           ("MO energy order and examples", [
              "For B2, C2, N2 (and Li2-N2): σ1s < σ*1s < σ2s < σ*2s < π2px = π2py < σ2pz < π*2px = π*2py < σ*2pz.",
              "For O2, F2, Ne2: σ2pz falls below π2p: ... σ2s < σ*2s < σ2pz < π2px = π2py < π*2px = π*2py < σ*2pz.",
              "H2: BO 1, diamagnetic. He2: BO 0 (not formed). N2: BO 3, diamagnetic. O2: BO 2, paramagnetic (two unpaired electrons in π*). O2⁺: BO 2.5; O2⁻: BO 1.5; F2: BO 1, diamagnetic. Stability order O2⁺ > O2 > O2⁻."]),
           ("Liquid crystals", [
              "Substances that flow like liquids but have molecular order like crystals, between melting point and clearing point.",
              "Thermotropic (temperature-dependent): nematic (thread-like, orientation order only), smectic (layered), cholesteric (twisted layers, colour changes with temperature). Lyotropic (concentration-dependent, e.g. soap solutions).",
              "Industrial materials: p-azoxyanisole, cholesteryl benzoate, MBBA. Uses: LCD displays, temperature sensors/thermometers, optical shutters."]),
           ("Graphite, fullerene and carbon nanotubes", [
              "Graphite: layers of sp² carbon hexagons, weak van der Waals forces between layers, delocalised π electrons → conducts electricity, soft, used as lubricant, electrodes, pencil lead.",
              "Fullerene C60 (buckminsterfullerene): football-shaped cage with 20 hexagons and 12 pentagons, sp² carbon, soluble in organic solvents. Used in drug delivery, lubricants, superconductors (K3C60), solar cells.",
              "Carbon nanotubes (CNT): rolled graphene sheets - single-walled (SWCNT) and multi-walled (MWCNT). Very high tensile strength, thermal and electrical conductivity; used in composites, sensors, electronics."]),
           ("Nanomaterials", [
              "Size 1-100 nm. Preparation: sol-gel, chemical vapour deposition, ball milling, laser ablation, electrodeposition.",
              "Characteristics: high surface area, quantum size effect, altered optical, magnetic and catalytic properties.",
              "Applications: catalysts, medicine, sensors, cosmetics, textiles, electronics, water treatment."]),
           ("Green chemistry - 12 principles", [
              "1 Prevent waste; 2 Atom economy; 3 Less hazardous chemical synthesis; 4 Designing safer chemicals; 5 Safer solvents and auxiliaries; 6 Design for energy efficiency;",
              "7 Use renewable feedstocks; 8 Reduce derivatives; 9 Catalysis (catalytic rather than stoichiometric reagents); 10 Design for degradation; 11 Real-time analysis to prevent pollution; 12 Inherently safer chemistry for accident prevention.",
              "Importance: reduces pollution and cost, protects health and environment. Green chemicals: water, supercritical CO2, ionic liquids, bio-based solvents (replacing toxic organic solvents)."]),
           ("Adipic acid and paracetamol - conventional vs green", [
              "Adipic acid (conventional): benzene → cyclohexane → cyclohexanol/cyclohexanone (KA oil) → oxidation with nitric acid → adipic acid; releases N2O (greenhouse gas) and uses toxic benzene.",
              "Adipic acid (green): from glucose using genetically engineered bacteria/biocatalysts, or oxidation of cyclohexene with 30% H2O2 using sodium tungstate catalyst - water is the by-product.",
              "Paracetamol (conventional): phenol → nitration → p-nitrophenol → reduction (Sn/HCl) → p-aminophenol → acetylation with acetic anhydride.",
              "Paracetamol (green): phenol + acetic anhydride (HF/catalyst) → 4-hydroxyacetophenone → oxime with hydroxylamine → Beckmann rearrangement → paracetamol; higher atom economy, fewer waste steps.",
              "Environmental impact: less hazardous waste, lower energy and safer processes."])],
          ["S: Define bond order and write its formula.", "S: Why is O2 paramagnetic?", "S: Write the MO electronic configuration of N2 and give its bond order.",
           "S: What are liquid crystals? Name their types.", "S: Draw the structure of C60 fullerene and state two uses.", "S: State any four principles of green chemistry.",
           "S: What is atom economy?",
           "L: Explain molecular orbital theory and draw the MO diagram of O2. Calculate its bond order and magnetic behaviour.",
           "L: Compare the bond order and magnetic nature of O2, O2⁺ and O2⁻.",
           "L: Discuss the types and applications of liquid crystals.",
           "L: Describe the structure and uses of graphite, fullerene and carbon nanotubes.",
           "L: What are nanomaterials? Discuss their preparation, properties and applications.",
           "L: Explain the twelve principles of green chemistry.",
           "L: Compare the conventional and green synthesis of adipic acid and paracetamol.",
           "N: Calculate the bond order of N2 and B2 using MO theory and predict their magnetic nature."]),

        U(2, "Spectroscopic Techniques and Stereochemistry", 8,
          "Spectroscopic techniques and applications: elementary idea and simple applications of UV, IR and NMR, numerical problems. Stereochemistry: optical isomerism in compounds without chiral carbon, geometrical isomerism, chiral drugs.",
          [("Basics of spectroscopy", [
              "Spectroscopy studies the interaction of electromagnetic radiation with matter. E = hv = hc/λ. Different regions cause different transitions: UV-Vis (electronic), IR (vibrational), radiofrequency in a magnetic field (NMR - nuclear spin).",
              "Beer-Lambert law: A = log(I0/I) = εcl (ε molar absorptivity, c concentration, l path length)."]),
           ("UV-Visible spectroscopy", [
              "Electronic transitions: σ→σ*, n→σ*, π→π*, n→π* (increasing wavelength order generally σ→σ* shortest).",
              "Chromophore: group that absorbs (C=C, C=O, NO2). Auxochrome (OH, NH2) deepens colour. Red/bathochromic shift = to longer λ; blue/hypsochromic shift = to shorter λ.",
              "Uses: concentration measurement, detecting conjugation, kinetics, purity check."]),
           ("IR spectroscopy", [
              "Molecule absorbs IR when a vibration changes its dipole moment (so N2, O2 are IR inactive). Stretching and bending vibrations.",
              "Typical positions (cm⁻¹): O-H 3200-3600 (broad), N-H 3300-3500, C-H 2850-3000, C≡C 2100-2260, C≡N 2220-2260, C=O 1650-1750 (strong), C=C 1600-1680.",
              "Uses: identify functional groups; fingerprint region (below 1500 cm⁻¹) identifies a compound."]),
           ("NMR spectroscopy", [
              "Nuclei with non-zero spin (1H, 13C) align in a magnetic field and absorb radiofrequency at resonance.",
              "Chemical shift δ (ppm) measured from tetramethylsilane (TMS, δ = 0): electronegative groups deshield protons (larger δ). Typical: alkyl 0.9-1.5, aromatic 6.5-8, aldehyde 9-10, -COOH 10-12.",
              "Number of signals = types of non-equivalent H; integration = ratio of H; spin-spin splitting follows the (n + 1) rule.",
              "Uses: structure determination, purity, MRI in medicine."]),
           ("Optical isomerism without a chiral carbon", [
              "Optical activity arises from molecular chirality (non-superimposable mirror image), not necessarily a chiral carbon.",
              "Allenes (R1R2C=C=CR3R4) with different groups on each end carbon show axial chirality. Ortho-substituted biphenyls (e.g. 6,6'-dinitro-2,2'-diphenic acid) are chiral due to restricted rotation (atropisomerism).",
              "Spiranes with appropriate substituents; compounds with chiral centres on N, S, P (e.g. sulfoxides, phosphines) are other examples."]),
           ("Geometrical isomerism", [
              "Arises from restricted rotation (C=C, C=N, rings). Cis (same side) - trans (opposite sides); E/Z using CIP priority rules: higher-priority groups same side = Z, opposite = E.",
              "Examples: maleic acid (cis) vs fumaric acid (trans); cis isomer is more polar, often higher boiling point and lower melting point than trans; oximes show syn/anti isomerism."]),
           ("Chiral drugs", [
              "Enantiomers have identical physical properties but can differ in biological effect because receptors are chiral.",
              "Examples: S-ibuprofen is the active anti-inflammatory; L-DOPA treats Parkinson's disease while D-DOPA is toxic; thalidomide - one enantiomer sedative, other teratogenic; S-naproxen, S-propranolol.",
              "Hence modern drugs are often made as single enantiomers (chiral switches)."])],
          ["S: State Beer-Lambert law.", "S: What is a chromophore? Give two examples.", "S: Which compounds are IR inactive? Why?",
           "S: What is chemical shift? Why is TMS used as reference?", "S: Give two examples of optically active compounds without a chiral carbon.",
           "S: Differentiate between E and Z isomers.", "S: Why are enantiomers important in drugs? Give an example.",
           "L: Explain the principle of UV-visible spectroscopy and the types of electronic transitions.",
           "L: Discuss the principle of IR spectroscopy and the factors required for a molecule to absorb IR radiation. List characteristic group frequencies.",
           "L: Explain the principle of NMR spectroscopy, chemical shift and spin-spin splitting.",
           "L: Explain optical isomerism in allenes and biphenyls.", "L: Discuss geometrical isomerism with examples and E-Z nomenclature.",
           "L: Write a note on chiral drugs.",
           "N: The absorbance of a 0.01 M solution in a 1 cm cell is 0.45. Calculate the molar absorptivity.",
           "N: Calculate the energy (in J) of IR radiation of wavenumber 1700 cm⁻¹."]),

        U(3, "Electrochemistry, Batteries, Corrosion and Cement", 8,
          "Electrochemistry and batteries: basic concepts of electrochemistry; classification and applications of primary cells (dry cell) and secondary cells (lead acid battery). Corrosion: introduction, types, cause, prevention and control, corrosion issues in specific industries (power generation, chemical processing, oil & gas, pulp & paper). Chemistry of engineering materials: cement - constituents, manufacturing, hardening and setting, deterioration of cement, Plaster of Paris (POP).",
          [("Electrochemistry basics", [
              "Galvanic cell converts chemical energy to electrical energy (spontaneous); electrolytic cell uses electrical energy to drive a non-spontaneous reaction. Oxidation at anode, reduction at cathode.",
              "EMF of cell = E°cathode - E°anode. Nernst equation: E = E° - (0.0591/n) log Q at 25 °C. Standard hydrogen electrode (SHE) is the reference (0 V).",
              "Higher (more positive) reduction potential → stronger oxidising agent."]),
           ("Batteries - classification", [
              "Primary cells: not rechargeable (dry cell, alkaline cell, mercury cell). Secondary cells: rechargeable (lead-acid, Ni-Cd, Li-ion). Reserve cells and fuel cells are other types."]),
           ("Dry (Leclanche) cell", [
              "Anode: zinc container; cathode: graphite rod surrounded by MnO2 + carbon; electrolyte: paste of NH4Cl + ZnCl2.",
              "Anode: Zn → Zn²⁺ + 2e⁻. Cathode: 2MnO2 + 2NH4⁺ + 2e⁻ → Mn2O3 + 2NH3 + H2O. EMF ≈ 1.5 V.",
              "Uses: torches, clocks, toys, remote controls."]),
           ("Lead-acid battery", [
              "Anode: spongy lead; cathode: PbO2 on lead grid; electrolyte: ~38% H2SO4 (density 1.2-1.3 g/cm³). Each cell ≈ 2 V; six cells give 12 V.",
              "Discharge: Pb + PbO2 + 2H2SO4 → 2PbSO4 + 2H2O (acid gets diluted). Charging reverses the reaction.",
              "Uses: automobiles, inverters, UPS, telephone exchanges."]),
           ("Corrosion - types, causes and control", [
              "Corrosion is the gradual destruction of metals by chemical or electrochemical attack of the environment (e.g. rusting of iron).",
              "Dry (chemical) corrosion by gases; wet (electrochemical) corrosion in presence of moisture/electrolyte. Types: uniform, galvanic, pitting, crevice, stress corrosion, intergranular, erosion.",
              "Causes: impurities in metal, contact of dissimilar metals, moisture, oxygen, acidic/saline medium.",
              "Prevention: protective coatings (paint, galvanising, tinning, electroplating), cathodic protection (sacrificial anode - Mg, Zn; impressed current), corrosion inhibitors, alloying (stainless steel), proper design, controlling environment.",
              "Industries: power plants (boiler water, cooling systems), chemical plants (acids, high temperature), oil and gas (H2S, CO2, pipelines), pulp and paper (chlorine and sulphur compounds)."]),
           ("Cement", [
              "Constituents: lime (CaO), silica (SiO2), alumina (Al2O3), iron oxide, gypsum (2-3%, controls setting). Main compounds: C3S (alite, early strength), C2S (belite, later strength), C3A, C4AF.",
              "Manufacture (dry/wet process): crush and grind limestone + clay → mix → heat in rotary kiln (1400-1500 °C) to form clinker → cool → grind with gypsum.",
              "Setting: stiffening of the paste by hydration (loss of plasticity). Hardening: gain of strength afterwards. Gypsum prevents flash set.",
              "Deterioration: sulphate attack, chloride-induced rebar corrosion, carbonation, alkali-silica reaction, freeze-thaw, acid attack."]),
           ("Plaster of Paris (POP)", [
              "Formula CaSO4·½H2O. Made by heating gypsum CaSO4·2H2O at 120-130 °C: CaSO4·2H2O → CaSO4·½H2O + 1½ H2O.",
              "On mixing with water it sets to hard gypsum, expanding slightly. Heating above ~200 °C gives anhydrous 'dead-burnt' plaster that does not set.",
              "Uses: plaster casts for fractures, statues and moulds, decorative ceilings, dental work."])],
          ["S: Write the Nernst equation.", "S: Differentiate between primary and secondary cells with examples.", "S: What is the EMF of a dry cell? Write its electrode reactions.",
           "S: What is the role of gypsum in cement?", "S: What is POP? Give its formula.", "S: What is sacrificial anode protection?",
           "L: Describe the construction, working and uses of the dry cell.", "L: Explain the construction and working of a lead-acid storage battery with reactions.",
           "L: What is corrosion? Explain the types of corrosion and the factors affecting it.",
           "L: Discuss the methods of prevention and control of corrosion.", "L: Write about corrosion problems in power generation, chemical, oil & gas and pulp & paper industries.",
           "L: Describe the manufacture of Portland cement and the chemistry of setting and hardening.", "L: Write a note on deterioration of cement.",
           "L: How is Plaster of Paris prepared? Give its setting reaction and uses.",
           "N: Calculate the EMF of a Zn-Cu cell at 25 °C with [Zn²⁺] = 0.1 M and [Cu²⁺] = 0.01 M (E°Zn = -0.76 V, E°Cu = +0.34 V)."]),

        U(4, "Water Technology and Fuels", 8,
          "Water technology: sources and impurities of water, hardness of water, boiler troubles, techniques for water softening (lime-soda, zeolite, ion exchange and reverse osmosis), determination of hardness and alkalinity, numerical problems. Fuels and combustion: definition, classification, characteristics of a good fuel, calorific values, gross and net calorific value, determination of calorific value by bomb calorimeter, theoretical calculation by Dulong's method, ranking of coal, analysis of coal by proximate and ultimate analysis, numerical problems, chemistry of biogas production from organic waste and environmental impact.",
          [("Sources and impurities of water", [
              "Sources: rain, surface (rivers, lakes), ground (wells, springs), sea water.",
              "Impurities: suspended (clay, sand), colloidal, dissolved (Ca, Mg salts, gases CO2, O2), biological (bacteria, algae)."]),
           ("Hardness of water", [
              "Hardness is caused by dissolved Ca²⁺ and Mg²⁺ salts that prevent soap from lathering.",
              "Temporary (carbonate) hardness: bicarbonates of Ca and Mg - removed by boiling. Permanent hardness: chlorides and sulphates of Ca and Mg - needs chemical treatment.",
              "Units: ppm (1 ppm = 1 mg/L), mg/L as CaCO3, °Clarke, °French. Equivalent of CaCO3 = (mass of salt x 100)/(molar mass of salt)."]),
           ("Boiler troubles", [
              "Scales and sludge: hard deposits (CaSO4, CaCO3, Mg(OH)2) lower heat transfer and cause overheating/explosion; sludge is soft, loose.",
              "Priming and foaming: carry-over of water with steam caused by dissolved salts and oils. Caustic embrittlement: cracks from NaOH in stressed joints. Boiler corrosion: dissolved O2, CO2, acids."]),
           ("Water softening methods", [
              "Lime-soda: lime Ca(OH)2 removes temporary hardness and Mg salts; soda Na2CO3 removes permanent Ca hardness. Cold and hot processes; hot is faster and gives lower residual hardness.",
              "Lime required L = (74/100)[Temp Ca + 2 x Temp Mg + Perm Mg + CO2 ...] and soda S = (106/100)[Perm Ca + Perm Mg ...] (all as CaCO3 equivalent, mg/L), multiplied by volume (basic form).",
              "Zeolite (permutit) process: hydrated sodium aluminosilicate Na2Z exchanges Na⁺ for Ca²⁺/Mg²⁺; exhausted zeolite is regenerated with 10% NaCl (brine).",
              "Ion-exchange: cation exchanger (RH) replaces Ca²⁺/Mg²⁺ by H⁺; anion exchanger (R'OH) replaces anions by OH⁻; H⁺ + OH⁻ → H2O gives demineralised water. Resins regenerated with acid/alkali.",
              "Reverse osmosis: water forced through a semi-permeable membrane under pressure greater than osmotic pressure, leaving salts behind; used in desalination and purifiers."]),
           ("Determination of hardness and alkalinity", [
              "EDTA method: sample + NH4Cl-NH4OH buffer (pH 10) + Eriochrome Black-T indicator; titrate with EDTA until wine red → blue.",
              "Alkalinity: titrate with standard acid. Phenolphthalein end point (P) and methyl orange end point (M) give OH⁻, CO3²⁻ and HCO3⁻ content: P = 0 → only HCO3⁻; P = ½M → only CO3²⁻; P = M → only OH⁻."]),
           ("Fuels and calorific value", [
              "Fuel: substance that burns to give heat. Classification: solid (coal, wood), liquid (petrol, diesel), gaseous (LPG, CNG, biogas); primary (natural) and secondary (derived).",
              "Good fuel: high calorific value, moderate ignition temperature, low ash and moisture, easy to store, safe, cheap, low pollution.",
              "Gross (higher) calorific value GCV: heat when products are cooled to room temperature (steam condensed). Net (lower) calorific value NCV = GCV - 0.09 x H x 587 cal/g (H = % hydrogen).",
              "Bomb calorimeter: weighed fuel is burned in oxygen at about 25 atm in a sealed bomb inside a water bath; GCV = [(W + w)(t2 - t1 + cooling correction) - (acid + fuse corrections)]/x.",
              "Dulong's formula: GCV = (1/100)[8080 C + 34500 (H - O/8) + 2240 S] kcal/kg."]),
           ("Coal ranking and analysis", [
              "Ranking: peat → lignite → bituminous → anthracite; carbon and calorific value increase, moisture and volatile matter decrease.",
              "Proximate analysis: moisture (105-110 °C, 1 h), volatile matter (925 ± 20 °C, 7 min in a covered crucible), ash (burn at 700-750 °C), fixed carbon = 100 - (%M + %VM + %Ash).",
              "Ultimate analysis: carbon and hydrogen by combustion (CO2 absorbed in KOH, H2O in CaCl2), nitrogen by Kjeldahl method, sulphur as BaSO4 (bomb washings), oxygen by difference."]),
           ("Biogas", [
              "Produced by anaerobic digestion of organic waste (cow dung, kitchen waste) by bacteria: hydrolysis → acidogenesis → acetogenesis → methanogenesis.",
              "Composition: CH4 55-65%, CO2 35-45%, traces of H2S, H2. Uses: cooking, lighting, electricity; the slurry is a good fertiliser.",
              "Environmental impact: reduces waste, methane capture, replaces fossil fuel and cuts GHG emissions."])],
          ["S: Differentiate between temporary and permanent hardness.", "S: What are the causes of priming and foaming?", "S: What is caustic embrittlement?",
           "S: Why is EDTA used for hardness determination? Name the indicator.", "S: Define GCV and NCV.", "S: List the characteristics of a good fuel.",
           "S: What is the importance of proximate analysis of coal?",
           "L: Explain the lime-soda process for water softening with reactions.", "L: Describe the zeolite process of water softening with regeneration.",
           "L: Explain the ion-exchange process for demineralisation of water.", "L: What is reverse osmosis? Discuss its principle and applications.",
           "L: Explain boiler troubles: scale, sludge, priming, foaming, caustic embrittlement and corrosion.",
           "L: Describe the determination of calorific value by bomb calorimeter.", "L: Explain proximate and ultimate analysis of coal and their significance.",
           "L: Discuss biogas production and its environmental benefits.",
           "N: A water sample contains Ca(HCO3)2 = 16.2 mg/L, Mg(HCO3)2 = 14.6 mg/L, CaSO4 = 13.6 mg/L. Calculate the temporary and permanent hardness.",
           "N: A coal sample has C = 80%, H = 5%, O = 8%, S = 1%. Find GCV by Dulong's formula and NCV.",
           "N: 0.95 g of a fuel raised the temperature of 2000 g of water from 25.0 °C to 27.5 °C. Water equivalent of calorimeter = 500 g. Find its calorific value (ignore corrections)."]),

        U(5, "Materials Chemistry and Organometallic Compounds", 8,
          "Polymers: classification, polymerization processes, thermosetting and thermoplastic polymers, polymer blends and composites, conducting and biodegradable polymers; preparation, properties and industrial applications of Teflon, Lucite, Bakelite, Kevlar, Dacron, Thiokol, Nylon, Buna-N and Buna-S and their environmental impact, speciality polymers. Organometallic compounds: general methods of preparation and applications of organometallic compounds (RMgX and LiAlH4).",
          [("Polymers - basics and classification", [
              "Polymer: giant molecule built from many repeating units (monomers). Degree of polymerisation n = molecular mass of polymer / molecular mass of monomer.",
              "Classification: natural / synthetic; linear / branched / cross-linked; homopolymer / copolymer; addition / condensation; thermoplastic / thermosetting; plastic / elastomer / fibre."]),
           ("Polymerisation processes", [
              "Addition (chain) polymerisation: free-radical mechanism with initiation (e.g. benzoyl peroxide), propagation, termination; no by-product (polyethylene, PVC, PTFE).",
              "Condensation (step) polymerisation: bifunctional monomers join with loss of small molecules such as H2O or HCl (nylon, Dacron, Bakelite).",
              "Coordination (Ziegler-Natta) polymerisation gives stereoregular polymers using TiCl4 + Al(C2H5)3."]),
           ("Thermoplastic vs thermosetting", [
              "Thermoplastic: linear/branched, soften on heating, can be remoulded, soluble, recyclable (PVC, polyethylene, nylon).",
              "Thermosetting: cross-linked 3-D network formed on heating, infusible and insoluble, cannot be remoulded (Bakelite, melamine, epoxy)."]),
           ("Blends, composites, conducting and biodegradable polymers", [
              "Polymer blend: physical mixture of two or more polymers giving improved properties (e.g. PC/ABS). Composite: a matrix (polymer) reinforced with fibres/particles (glass-fibre reinforced plastic, carbon-fibre composites) - high strength, low weight.",
              "Conducting polymers: conjugated polymers made conductive by doping - polyacetylene (doped with I2), polyaniline, polypyrrole; used in batteries, sensors, antistatic coatings, LEDs.",
              "Biodegradable polymers decompose by microbes: PLA (polylactic acid), PHB/PHBV, polycaprolactone; used in packaging, sutures, drug delivery."]),
           ("Preparation, properties and uses of important polymers", [
              "Teflon (PTFE): free-radical polymerisation of tetrafluoroethylene CF2=CF2; very high chemical resistance, low friction, stable to ~260 °C; non-stick cookware, gaskets, seals.",
              "Lucite (PMMA): addition polymerisation of methyl methacrylate; transparent, light, weather-resistant; used for lenses, aircraft windows, signboards.",
              "Bakelite: condensation of phenol with formaldehyde (acid or base catalyst) → novolac/resol → cross-linked thermosetting; hard, heat and electrical insulator; switches, handles, laminates.",
              "Kevlar: condensation of p-phenylenediamine with terephthaloyl chloride (aromatic polyamide/aramid); very high tensile strength; bullet-proof vests, tyres, aerospace.",
              "Dacron (PET/polyester): condensation of ethylene glycol with terephthalic acid (or dimethyl terephthalate); strong, wrinkle resistant; fibres, bottles.",
              "Thiokol (polysulfide rubber): ethylene dichloride + sodium polysulfide; resistant to oils and solvents; hoses, gaskets, sealants, rocket fuel binder.",
              "Nylon-6,6: hexamethylenediamine + adipic acid; Nylon-6: ring-opening polymerisation of caprolactam; used in fibres, ropes, gears.",
              "Buna-N (NBR): butadiene + acrylonitrile; oil resistant; oil seals, hoses. Buna-S (SBR): butadiene + styrene; abrasion resistant; tyres.",
              "Environmental impact: persistence of non-biodegradable plastics, microplastics, toxic fumes from burning; reduce by recycling, biodegradable alternatives, proper disposal.",
              "Speciality polymers: ion-exchange resins, polymer electrolytes, liquid-crystal polymers, hydrogels, shape-memory polymers."]),
           ("Organometallic compounds - Grignard reagent and LiAlH4", [
              "Organometallic compounds contain a metal-carbon bond. Grignard reagent RMgX: R-X + Mg → RMgX in dry diethyl ether (moisture destroys it).",
              "Uses of RMgX: with HCHO → primary alcohol; with other aldehydes → secondary alcohols; with ketones → tertiary alcohols; with CO2 → carboxylic acids; with epoxides → alcohols; with water → alkane.",
              "LiAlH4 (lithium aluminium hydride): 4LiH + AlCl3 → LiAlH4 + 3LiCl in dry ether. A powerful reducing agent: reduces aldehydes, ketones, esters, carboxylic acids to alcohols; amides and nitriles to amines. Reacts violently with water."])],
          ["S: What are thermoplastic and thermosetting polymers? Give examples.", "S: What is a composite? Give an example.", "S: What are conducting polymers?",
           "S: Write the monomers of Buna-S and Nylon-6,6.", "S: What is a biodegradable polymer? Give two examples.", "S: Write two uses of the Grignard reagent.",
           "L: Classify polymers and explain addition and condensation polymerisation.", "L: Distinguish between thermoplastic and thermosetting polymers.",
           "L: Discuss polymer blends, composites, conducting and biodegradable polymers.",
           "L: Give the preparation, properties and uses of Teflon, Lucite and Bakelite.", "L: Give the preparation, properties and uses of Kevlar, Dacron and Thiokol.",
           "L: Explain the preparation and uses of Nylon, Buna-N and Buna-S and their environmental impact.",
           "L: Describe the preparation and applications of Grignard reagent.", "L: Describe the preparation and applications of lithium aluminium hydride.",
           "N: A polymer has an average molecular mass of 28,000 and monomer mass 28. Find the degree of polymerisation."]),
    ],
    labs=[{"code": "BAS152 / BAS252", "title": "Engineering Chemistry Lab (instructor selects any 10 experiments)", "items": [
        "Calibration of analytical equipment and apparatus", "Hardness of water by EDTA method", "Alkalinity of a water sample", "pH by titrimetric method",
        "Surface tension of a liquid", "Viscosity of a liquid by viscometer", "Strength of ferrous ammonium sulphate using external indicator",
        "Strength of potassium dichromate using internal indicator", "Available chlorine in bleaching powder", "Chloride content in water",
        "Preparation of phenol-formaldehyde resin", "Preparation of urea-formaldehyde resin", "Preparation of adipic acid / paracetamol",
        "Cell conductance of a solution", "Rate constant of hydrolysis of an ester", "Element detection and functional groups in organic compounds"]}],
)

SUBJECTS = [PHYSICS, CHEMISTRY]
