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
  els.packageExplanation.textContent = 'AI presents one package, but every hotel night, ride, meal, discount, product, provider, expiration, and receipt remains a separate typed claim underneath.'
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
  bindNavigation()
  els.form?.addEventListener('submit', buildPackage)
  ;[els.destinationType, els.tripLength, els.includeAccessibility, els.includeNfc, els.includeProducts]
    .forEach(control => control?.addEventListener('change', buildPackage))
  els.year.textContent = new Date().getFullYear()
  buildPackage()
}

init()
