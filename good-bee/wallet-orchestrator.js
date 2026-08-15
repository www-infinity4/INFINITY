const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  form: document.querySelector('#packageForm'),
  destinationType: document.querySelector('#destinationType'),
  tripLength: document.querySelector('#tripLength'),
  includeAccessibility: document.querySelector('#includeAccessibility'),
  includeNfc: document.querySelector('#includeNfc'),
  includeProducts: document.querySelector('#includeProducts'),
  packageTitle: document.querySelector('#packageTitle'),
  packageRows: document.querySelector('#packageRows'),
  packageExplanation: document.querySelector('#packageExplanation'),
  graphSection: document.querySelector('#graph'),
  year: document.querySelector('#year')
}

const destinationNames = {
  beach: 'beach',
  mountain: 'mountain',
  city: 'city',
  sailing: 'sailing'
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function buildPackage(event) {
  event?.preventDefault()

  const destination = destinationNames[els.destinationType.value] || 'travel'
  const days = Number(els.tripLength.value) || 7
  const hotelNights = days
  const hotelUnits = hotelNights * 100
  const rows = [
    ['Destination package', `${days}-day ${destination} plan`],
    ['Hotel claims', `${hotelNights} nights / ${hotelUnits} example Infinity units`],
    ['Transportation', `${Math.max(2, Math.ceil(days / 3))} ride claims`],
    ['Meals', `${days * 2} meal claims`]
  ]

  if (els.includeAccessibility.checked) {
    rows.push(['Accessibility coordination', 'Room, transport, communication, activity, and support review'])
  }

  if (els.includeNfc.checked) {
    rows.push(['NFC baseline', '$0.50-equivalent participating scan discount'])
    rows.push(['In-person offers', 'Local merchant and immediate-fulfillment bonuses compared automatically'])
  }

  if (els.includeProducts.checked) {
    const products = destination === 'beach'
      ? 'sun protection, accessible beach equipment, hydration, luggage support'
      : destination === 'mountain'
        ? 'weather layer, hydration, altitude planning, trail or mobility equipment'
        : destination === 'sailing'
          ? 'weather gear, adaptive sailing review, hydration, communications'
          : 'transit pass, event access, luggage support, local essentials'
    rows.push(['Useful product claims', products])
  }

  els.packageTitle.textContent = `${days}-day ${destination} package`
  els.packageRows.innerHTML = rows.map(([label, value]) => `
    <div class="package-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>
  `).join('')
  els.packageExplanation.textContent = 'AI presents one package, but every Star version, Product Token, Avatar identity, hotel night, ride, meal, discount, product, provider, expiration, and receipt remains a separate typed record underneath.'
}

function integrateTokenStudio() {
  if (els.mainNav && !els.mainNav.querySelector('a[href="token-studio.html"]')) {
    const link = document.createElement('a')
    link.href = 'token-studio.html'
    link.textContent = '⭐ Token Studio'
    const plannerLink = els.mainNav.querySelector('a[href="coin-planner.html"]')
    els.mainNav.insertBefore(link, plannerLink || null)
  }

  if (!els.graphSection || document.querySelector('#token-studio')) return

  const section = document.createElement('section')
  section.id = 'token-studio'
  section.className = 'section business-section'
  section.innerHTML = `
    <div class="section-heading">
      <div><p class="eyebrow">Infinity AI Token Studio</p><h2>The wallet now understands creation before commerce.</h2></div>
      <p>Click the same subtle upper-right ⭐ on any convertible object to create a named version, define the Product Token the system needs, calculate supply, and determine whether the product requires an Avatar Coin identity.</p>
    </div>
    <div class="business-layout">
      <div class="business-coin">
        <span>UNIVERSAL CREATION MARK</span>
        <strong>⭐ STAR → PRODUCT → AVATAR</strong>
        <small>Versioned · typed · attributable</small>
      </div>
      <div class="business-spec">
        <article><h3>Star Blueprint</h3><p>Named, editable child version with parent ancestry. Earlier work remains visible.</p></article>
        <article><h3>Product Token</h3><p>The exact product, service, station, component, package, offer, or work role Infinity needs produced.</p></article>
        <article><h3>Avatar Coin</h3><p>Identity activation for products such as radio stations or businesses. One coin locks to one active identity.</p></article>
        <article><h3>Store Claim</h3><p>Created only after provider, capacity, funding, restrictions, fulfillment, refund, and rights verification.</p></article>
        <article><h3>Need charts</h3><p>System demand, scarcity, human usefulness, production readiness, and local capacity remain visible.</p></article>
        <article><h3>Open Studio</h3><p><a class="button primary" href="token-studio.html">⭐ Create or convert a token</a></p></article>
      </div>
    </div>
  `

  els.graphSection.before(section)
}

function integrateCoinPlanner() {
  if (els.mainNav && !els.mainNav.querySelector('a[href="coin-planner.html"]')) {
    const link = document.createElement('a')
    link.href = 'coin-planner.html'
    link.textContent = 'Coin Planner'
    const clearingLink = els.mainNav.querySelector('a[href="reciprocal-clearing.html"]')
    els.mainNav.insertBefore(link, clearingLink || null)
  }

  if (!els.graphSection || document.querySelector('#coin-planner')) return

  const section = document.createElement('section')
  section.id = 'coin-planner'
  section.className = 'section products-section'
  section.innerHTML = `
    <div class="section-heading">
      <div><p class="eyebrow">Infinity Coin Planner</p><h2>Search globally, buy locally and in bulk, then close the package funding gap.</h2></div>
      <p>Coin Planner consumes Product Token needs, discovers businesses through permitted sources, verifies merchant control and live capacity, negotiates local contracts, forecasts destination demand, stages appropriate products, and combines the results into Store Card packages.</p>
    </div>
    <div class="package-builder">
      <div class="package-form">
        <strong>$1,000 benchmark → 100-unit target</strong>
        <p>The retail-equivalent benchmark does not pay the provider. The planner separately shows contracted cost, traveler units, sponsor funding, program funding, Infinity funding, and any remaining gap.</p>
        <a class="button primary" href="coin-planner.html">Open Coin Planner</a>
      </div>
      <div class="package-output">
        <p class="eyebrow">Planner chain</p>
        <h3>Product need → discover → verify → negotiate → stage → package → fund → fulfill</h3>
        <div class="package-row"><span>Business coverage</span><strong>Multiple official, licensed, open, and merchant-direct sources</strong></div>
        <div class="package-row"><span>Source order</span><strong>Local destination businesses first</strong></div>
        <div class="package-row"><span>Publication rule</span><strong>No package while a funding gap remains</strong></div>
      </div>
    </div>
  `

  els.graphSection.before(section)
}

function bindNavigation() {
  els.menuButton?.addEventListener('click', () => {
    const open = els.mainNav.classList.toggle('open')
    els.menuButton.setAttribute('aria-expanded', String(open))
  })

  els.mainNav?.addEventListener('click', event => {
    if (event.target.matches('a')) {
      els.mainNav.classList.remove('open')
      els.menuButton?.setAttribute('aria-expanded', 'false')
    }
  })
}

function init() {
  integrateTokenStudio()
  integrateCoinPlanner()
  bindNavigation()
  els.form?.addEventListener('submit', buildPackage)
  ;[els.destinationType, els.tripLength, els.includeAccessibility, els.includeNfc, els.includeProducts]
    .forEach(control => control?.addEventListener('change', buildPackage))
  els.year.textContent = new Date().getFullYear()
  buildPackage()
}

init()
