const DATA_URL = './data/store-cards.json'
const TOKEN_KEY = 'msw_tokens'
const IGNITION_KEY = 'ign_tok'
const COIN_KEY = 'msw_coins'
const CAPACITOR_KEY = 'msw_capacitor'

const state = {
  data: null,
  tokens: readJson(TOKEN_KEY, []),
  coins: readNumber(COIN_KEY, 0),
  capacitor: readNumber(CAPACITOR_KEY, 0.5)
}

const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  cardGrid: document.querySelector('#cardGrid'),
  marketSearch: document.querySelector('#marketSearch'),
  marketCategory: document.querySelector('#marketCategory'),
  marketCard: document.querySelector('#marketCard'),
  marketStatus: document.querySelector('#marketStatus'),
  offerGrid: document.querySelector('#offerGrid'),
  trainingOffer: document.querySelector('#trainingOffer'),
  demoCoins: document.querySelector('#demoCoins'),
  demoTokens: document.querySelector('#demoTokens'),
  demoCapacitor: document.querySelector('#demoCapacitor'),
  consoleLog: document.querySelector('#consoleLog'),
  tokenTray: document.querySelector('#tokenTray'),
  consoleActions: document.querySelector('.console-actions'),
  moduleGrid: document.querySelector('#moduleGrid'),
  year: document.querySelector('#year')
}

function readJson(key, fallback) {
  try {
    const value = JSON.parse(localStorage.getItem(key))
    return Array.isArray(value) ? value : fallback
  } catch {
    return fallback
  }
}

function readNumber(key, fallback) {
  const value = Number(localStorage.getItem(key))
  return Number.isFinite(value) ? value : fallback
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

async function fetchData() {
  const response = await fetch(DATA_URL, { headers: { Accept: 'application/json' } })
  if (!response.ok) throw new Error(`Store-card data unavailable (${response.status})`)
  return response.json()
}

function renderCards() {
  els.cardGrid.innerHTML = state.data.cards.map(card => `
    <article class="store-system-card" id="card-${escapeHtml(card.id)}">
      <div class="card-chip" aria-hidden="true"></div>
      <span class="family">${escapeHtml(card.family)}</span>
      <h3>${escapeHtml(card.name)}</h3>
      <p>${escapeHtml(card.purpose)}</p>
      <div class="surface"><strong>Physical/digital form:</strong> ${escapeHtml(card.surface)}</div>
      <ul>${card.protections.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      <div class="store-list">${card.stores.map(store => `<span>${escapeHtml(store)}</span>`).join('')}</div>
    </article>
  `).join('')
}

function populateFilters() {
  const categories = [...new Set(state.data.offers.map(offer => offer.category))].sort()
  els.marketCategory.insertAdjacentHTML('beforeend', categories.map(category => `<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`).join(''))
  els.marketCard.insertAdjacentHTML('beforeend', state.data.cards.map(card => `<option value="${escapeHtml(card.id)}">${escapeHtml(card.name)}</option>`).join(''))
  els.trainingOffer.innerHTML = state.data.offers.map(offer => `<option value="${escapeHtml(offer.id)}">${escapeHtml(offer.name)}</option>`).join('')
}

function cardName(id) {
  return state.data.cards.find(card => card.id === id)?.name || id
}

function renderOffers() {
  const query = els.marketSearch.value.trim().toLowerCase()
  const category = els.marketCategory.value
  const selectedCard = els.marketCard.value

  const offers = state.data.offers.filter(offer => {
    const searchable = [offer.name, offer.store, offer.category, offer.priceLabel, offer.status, offer.risk, ...offer.cardFamilies.map(cardName)].join(' ').toLowerCase()
    return (!query || searchable.includes(query))
      && (category === 'all' || offer.category === category)
      && (selectedCard === 'all' || offer.cardFamilies.includes(selectedCard))
  })

  els.marketStatus.textContent = `Showing ${offers.length} of ${state.data.offers.length} public prototype offers.`
  els.offerGrid.innerHTML = offers.length ? offers.map(offer => `
    <article class="offer-card">
      <div class="offer-meta"><span>${escapeHtml(offer.store)}</span><span>${escapeHtml(offer.status)}</span></div>
      <h3>${escapeHtml(offer.name)}</h3>
      <span>${escapeHtml(offer.category)}</span>
      <div class="price-label">${escapeHtml(offer.priceLabel)}</div>
      <div class="card-tags">${offer.cardFamilies.map(id => `<span>${escapeHtml(cardName(id))}</span>`).join('')}</div>
      <p class="risk-note"><strong>Review before approval:</strong> ${escapeHtml(offer.risk)}</p>
    </article>
  `).join('') : '<p>No offers match this search.</p>'
}

function renderModules() {
  els.moduleGrid.innerHTML = state.data.modules.map(module => `
    <article class="module-card">
      <h3>${escapeHtml(module.name)}</h3>
      <p>${escapeHtml(module.role)}</p>
    </article>
  `).join('')
}

function saveDemo() {
  localStorage.setItem(TOKEN_KEY, JSON.stringify(state.tokens))
  localStorage.setItem(IGNITION_KEY, String(state.tokens.length))
  localStorage.setItem(COIN_KEY, String(state.coins))
  localStorage.setItem(CAPACITOR_KEY, String(state.capacitor))
}

function renderDemo() {
  els.demoCoins.textContent = String(state.coins)
  els.demoTokens.textContent = String(state.tokens.length)
  els.demoCapacitor.textContent = state.capacitor.toFixed(1)
  els.tokenTray.innerHTML = state.tokens.slice(-14).reverse().map(token => `<span>${escapeHtml(token)}</span>`).join('')
}

function selectedOffer() {
  return state.data.offers.find(offer => offer.id === els.trainingOffer.value) || state.data.offers[0]
}

function mintToken(label) {
  state.tokens.push(label)
  if (state.tokens.length > 250) state.tokens = state.tokens.slice(-250)
}

function setLog(message) {
  els.consoleLog.textContent = message
}

function act(action) {
  const offer = selectedOffer()
  if (!offer) return

  switch (action) {
    case 'grab':
      mintToken(`GRAB: ${offer.name}`)
      setLog(`GRABBED ${offer.name}. A named demonstration token was added to the local Shop World wallet.`)
      break
    case 'accept':
      state.coins += 5
      mintToken(`ACCEPT: ${offer.name}`)
      setLog(`ACCEPTED ${offer.name}. Added 5 demonstration coins. In real commerce, acceptance would still require price, payment, identity, and fulfillment confirmation.`)
      break
    case 'reject':
      state.coins += 3
      mintToken(`REJECT: ${offer.name}`)
      setLog(`REJECTED ${offer.name}. Added 3 demonstration coins for identifying or declining a poor fit.`)
      break
    case 'charge':
      state.capacitor = Math.min(1, Number((state.capacitor + 0.2).toFixed(1)))
      mintToken('? BLOCK')
      setLog('CAPACITOR CHARGED +0.2. The earlier ? BLOCK mechanic is preserved as a demonstration token.')
      break
    case 'bid':
      if (state.capacitor < 0.2) {
        setLog('BID BLOCKED. The bid capacitor must be at least 0.2.')
        return
      }
      state.capacitor = Math.max(0, Number((state.capacitor - 0.3).toFixed(1)))
      mintToken(`BID: ${offer.name}`)
      setLog(`DEMO BID recorded for ${offer.name}. Consumed 0.3 capacitor. No payment or external bid was placed.`)
      break
    case 'reset':
      state.tokens = []
      state.coins = 0
      state.capacitor = 0.5
      setLog('Local Shop World demonstration wallet reset. No real account or value was affected.')
      break
    default:
      return
  }

  saveDemo()
  renderDemo()
}

function bindEvents() {
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

  ;[els.marketSearch, els.marketCategory, els.marketCard].forEach(control => {
    control?.addEventListener(control === els.marketSearch ? 'input' : 'change', renderOffers)
  })

  els.consoleActions?.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]')
    if (button) act(button.dataset.action)
  })
}

async function init() {
  els.year.textContent = new Date().getFullYear()
  bindEvents()

  try {
    state.data = await fetchData()
    renderCards()
    populateFilters()
    renderOffers()
    renderModules()
    renderDemo()
  } catch (error) {
    els.marketStatus.textContent = error.message
    els.cardGrid.innerHTML = `<p role="alert">${escapeHtml(error.message)}</p>`
  }
}

init()
