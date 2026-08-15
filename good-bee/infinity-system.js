const DATA_URL = './data/system-map.json'

const state = { data: null }

const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  moduleSearch: document.querySelector('#moduleSearch'),
  categoryFilter: document.querySelector('#categoryFilter'),
  moduleStatus: document.querySelector('#moduleStatus'),
  moduleGrid: document.querySelector('#moduleGrid'),
  valueGrid: document.querySelector('#valueGrid'),
  ruleGrid: document.querySelector('#ruleGrid'),
  year: document.querySelector('#year')
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
  if (!response.ok) throw new Error(`System map unavailable (${response.status})`)
  return response.json()
}

function populateCategories() {
  const categories = [...new Set(state.data.modules.map(module => module.category))].sort()
  els.categoryFilter.insertAdjacentHTML('beforeend', categories.map(category => `
    <option value="${escapeHtml(category)}">${escapeHtml(category)}</option>
  `).join(''))
}

function renderModules() {
  const query = els.moduleSearch.value.trim().toLowerCase()
  const category = els.categoryFilter.value

  const modules = state.data.modules.filter(module => {
    const searchable = [module.name, module.category, module.purpose, ...module.inputs, ...module.outputs].join(' ').toLowerCase()
    return (!query || searchable.includes(query)) && (category === 'all' || module.category === category)
  })

  els.moduleStatus.textContent = `Showing ${modules.length} of ${state.data.modules.length} connected modules.`
  els.moduleGrid.innerHTML = modules.length ? modules.map(module => `
    <article class="system-module-card">
      <span class="category">${escapeHtml(module.category)}</span>
      <h3>${escapeHtml(module.name)}</h3>
      <p>${escapeHtml(module.purpose)}</p>
      <div class="io">
        <div><strong>Inputs</strong><span>${module.inputs.map(escapeHtml).join(' · ')}</span></div>
        <div><strong>Outputs</strong><span>${module.outputs.map(escapeHtml).join(' · ')}</span></div>
      </div>
      <a class="button primary" href="${escapeHtml(module.url)}">Open module</a>
    </article>
  `).join('') : '<p>No system modules match this search.</p>'
}

function renderValueTypes() {
  els.valueGrid.innerHTML = state.data.valueTypes.map((type, index) => `
    <article class="value-card">
      <span>${String(index + 1).padStart(2, '0')}</span>
      <h3>${escapeHtml(type.name)}</h3>
      <p>${escapeHtml(type.meaning)}</p>
    </article>
  `).join('')
}

function renderRules() {
  els.ruleGrid.innerHTML = state.data.coreRules.map((rule, index) => `
    <article class="rule-card">
      <strong>Rule ${String(index + 1).padStart(2, '0')}</strong>
      <span>${escapeHtml(rule)}</span>
    </article>
  `).join('')
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

  els.moduleSearch?.addEventListener('input', renderModules)
  els.categoryFilter?.addEventListener('change', renderModules)
}

async function init() {
  els.year.textContent = new Date().getFullYear()
  bindEvents()

  try {
    state.data = await fetchData()
    populateCategories()
    renderModules()
    renderValueTypes()
    renderRules()
  } catch (error) {
    els.moduleStatus.textContent = error.message
    els.moduleGrid.innerHTML = `<p role="alert">${escapeHtml(error.message)}</p>`
  }
}

init()
