const DATA_URL = './data/token-studio.json'
const STORAGE_KEY = 'infinity_token_studio_v1'

const state = {
  data: null,
  selected: null,
  local: loadLocal()
}

const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  moduleGrid: document.querySelector('#moduleGrid'),
  rankingChart: document.querySelector('#rankingChart'),
  tokenForm: document.querySelector('#tokenForm'),
  selectedObject: document.querySelector('#selectedObject'),
  creationName: document.querySelector('#creationName'),
  productDefinition: document.querySelector('#productDefinition'),
  systemNeed: document.querySelector('#systemNeed'),
  plannedUnits: document.querySelector('#plannedUnits'),
  identityProduct: document.querySelector('#identityProduct'),
  factorControls: document.querySelector('#factorControls'),
  planTitle: document.querySelector('#planTitle'),
  priorityBadge: document.querySelector('#priorityBadge'),
  planRows: document.querySelector('#planRows'),
  factorChart: document.querySelector('#factorChart'),
  supplyChart: document.querySelector('#supplyChart'),
  versionList: document.querySelector('#versionList'),
  eventList: document.querySelector('#eventList'),
  resetLedger: document.querySelector('#resetLedger'),
  year: document.querySelector('#year')
}

function loadLocal() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null')
    if (parsed?.schemaVersion === '1.0.0' && Array.isArray(parsed.versions) && Array.isArray(parsed.events)) return parsed
  } catch (_) {}
  return { schemaVersion: '1.0.0', versions: [], events: [] }
}

function saveLocal() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.local))
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function uid(prefix) {
  const random = crypto.getRandomValues(new Uint32Array(2))
  return `${prefix}-${Date.now().toString(36)}-${random[0].toString(36)}${random[1].toString(36)}`
}

function addEvent(type, detail, amount = '') {
  state.local.events.unshift({ id: uid('event'), type, detail, amount, createdAt: new Date().toISOString() })
  state.local.events = state.local.events.slice(0, 250)
}

async function fetchData() {
  const response = await fetch(DATA_URL, { headers: { Accept: 'application/json' } })
  if (!response.ok) throw new Error(`Token Studio data unavailable (${response.status})`)
  return response.json()
}

function weights() {
  return state.data?.needWeights || {
    systemDemand: 35,
    scarcity: 25,
    humanUsefulness: 20,
    productionReadiness: 10,
    localCapacity: 10
  }
}

function factorLabels() {
  return {
    systemDemand: 'System demand',
    scarcity: 'Scarcity',
    humanUsefulness: 'Human usefulness',
    productionReadiness: 'Production readiness',
    localCapacity: 'Local capacity'
  }
}

function calculateScore(scores) {
  const currentWeights = weights()
  return Number(Object.entries(currentWeights).reduce((total, [id, weight]) => {
    return total + (Number(scores[id]) || 0) * weight / 100
  }, 0).toFixed(1))
}

function priorityFor(score) {
  if (score >= 80) return 'Critical product priority'
  if (score >= 60) return 'High product priority'
  if (score >= 40) return 'Build and verify'
  return 'Research before production'
}

function priorityColor(score) {
  if (score >= 80) return '#ff5a74'
  if (score >= 60) return '#ffe600'
  if (score >= 40) return '#00fff7'
  return '#8fa5ba'
}

function addStarMark(target) {
  if (!target || target.querySelector(':scope > .conversion-star')) return
  target.classList.add('convertible')
  const button = document.createElement('button')
  button.type = 'button'
  button.className = 'conversion-star'
  button.textContent = '⭐'
  const label = target.dataset.convertLabel || target.querySelector('h3,h4,strong')?.textContent?.trim() || 'convertible object'
  button.title = `Create, edit, version or convert ${label}`
  button.setAttribute('aria-label', `Open Token Studio for ${label}`)
  button.addEventListener('click', event => {
    event.preventDefault()
    event.stopPropagation()
    selectConvertible({
      id: target.dataset.convertId || uid('object'),
      type: target.dataset.convertType || 'object',
      label,
      element: target
    })
  })
  target.appendChild(button)
}

function markAllConvertible(root = document) {
  root.querySelectorAll('.convertible').forEach(addStarMark)
}

function renderFactorControls() {
  const labels = factorLabels()
  els.factorControls.innerHTML = Object.entries(weights()).map(([id, weight]) => `
    <div class="factor-control">
      <label for="factor-${escapeHtml(id)}">${escapeHtml(labels[id])} · ${weight}% weight</label>
      <input id="factor-${escapeHtml(id)}" data-factor="${escapeHtml(id)}" type="range" min="0" max="100" value="50">
      <output id="output-${escapeHtml(id)}">50</output>
    </div>
  `).join('')

  els.factorControls.querySelectorAll('[data-factor]').forEach(input => {
    input.addEventListener('input', () => {
      els.factorControls.querySelector(`#output-${CSS.escape(input.dataset.factor)}`).textContent = input.value
      renderPlan()
    })
  })
}

function rankedModules() {
  return [...(state.data?.modules || [])]
    .map(module => ({ ...module, calculatedScore: calculateScore(module.scores) }))
    .sort((a, b) => b.calculatedScore - a.calculatedScore)
}

function renderModules() {
  const modules = rankedModules()
  els.moduleGrid.innerHTML = modules.map((module, index) => `
    <article class="need-module convertible" data-module-id="${escapeHtml(module.id)}" data-convert-id="${escapeHtml(module.id)}" data-convert-type="module" data-convert-label="${escapeHtml(module.name)}">
      <span class="module-category">${String(index + 1).padStart(2, '0')} · ${escapeHtml(module.category)}</span>
      <h3>${escapeHtml(module.name)}</h3>
      <p>${escapeHtml(module.systemNeed)}</p>
      <button type="button" class="button secondary use-example">Use this example</button>
      <div class="score-row">
        <span>${escapeHtml(priorityFor(module.calculatedScore))}</span>
        <strong>${module.calculatedScore}</strong>
      </div>
    </article>
  `).join('')

  els.moduleGrid.querySelectorAll('[data-module-id]').forEach(card => {
    card.addEventListener('click', event => {
      if (event.target.closest('.conversion-star')) return
      selectModule(card.dataset.moduleId)
    })
  })
  markAllConvertible(els.moduleGrid)
  drawRankingChart(modules)
}

function selectModule(id) {
  const module = state.data.modules.find(item => item.id === id)
  if (!module) return
  state.selected = { kind: 'module', id: module.id, label: module.name, module }
  document.querySelector('#templateSelect').value = module.id
  els.selectedObject.value = `Example: ${module.name}`
  els.creationName.value = module.name
  els.productDefinition.value = module.productToken
  els.systemNeed.value = module.systemNeed
  els.plannedUnits.value = module.plannedIdentities
  els.identityProduct.checked = module.identityProduct
  Object.entries(module.scores).forEach(([factor, value]) => {
    const input = els.factorControls.querySelector(`[data-factor="${CSS.escape(factor)}"]`)
    const output = els.factorControls.querySelector(`#output-${CSS.escape(factor)}`)
    if (input) input.value = value
    if (output) output.textContent = value
  })
  renderPlan()
  document.querySelector('#studio').scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function selectConvertible(context) {
  const saved = state.local.versions.find(item => item.id === context.id)
  if (saved) { selectSavedVersion(saved); return }
  const module = state.data?.modules.find(item => item.id === context.id)
  if (module) {
    selectModule(module.id)
    return
  }

  state.selected = { kind: context.type, id: context.id, label: context.label, module: null }
  els.selectedObject.value = `${context.type}: ${context.label}`
  els.creationName.value = context.label
  els.productDefinition.value = ''
  els.systemNeed.value = ''
  els.plannedUnits.value = 1
  els.identityProduct.checked = ['business', 'station', 'avatar-coin'].includes(context.type)
  els.factorControls.querySelectorAll('[data-factor]').forEach(input => {
    input.value = 50
    els.factorControls.querySelector(`#output-${CSS.escape(input.dataset.factor)}`).textContent = 50
  })
  renderPlan()
  document.querySelector('#studio').scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function formValues() {
  const scores = {}
  els.factorControls.querySelectorAll('[data-factor]').forEach(input => {
    scores[input.dataset.factor] = Number(input.value)
  })
  return {
    selectedObject: els.selectedObject.value || 'Unselected object',
    name: els.creationName.value.trim() || 'Untitled creation',
    productToken: els.productDefinition.value.trim() || 'Product definition required',
    systemNeed: els.systemNeed.value.trim() || 'System need required',
    plannedUnits: Math.max(1, Math.min(1000000, Math.floor(Number(els.plannedUnits.value) || 1))),
    identityProduct: els.identityProduct.checked,
    scores
  }
}

function buildPlan(values) {
  const score = calculateScore(values.scores)
  const reserve = Math.max(1, Math.ceil(values.plannedUnits * 0.2))
  const productSupply = values.plannedUnits + reserve
  const weakest = Object.entries(values.scores).sort((a, b) => a[1] - b[1])[0]
  const labels = factorLabels()
  return {
    score,
    priority: priorityFor(score),
    reserve,
    productSupply,
    avatarRequired: values.identityProduct ? values.plannedUnits : 0,
    weakestId: weakest[0],
    weakestValue: weakest[1],
    weakestLabel: labels[weakest[0]],
    nextAction: weakest[1] < 60
      ? `Raise ${labels[weakest[0]].toLowerCase()} with evidence, verified capacity, or a qualified partner before scaling.`
      : 'Save the named version, verify production capacity, and connect fulfillment evidence.'
  }
}

function renderPlan() {
  if (!els.planRows) return
  const values = formValues()
  const plan = buildPlan(values)

  els.planTitle.textContent = els.creationName.value.trim() || 'Your idea will appear here'
  document.querySelector('#draftSummary').textContent = `What you’re making: ${els.productDefinition.value.trim() || 'Describe your product or service.'}\n\nWho it helps: ${els.systemNeed.value.trim() || 'Explain who needs it and why.'}\n\nPlanned quantity: ${values.plannedUnits}\n\nSaving creates a draft on this browser only.`
  els.priorityBadge.textContent = `${plan.priority} · ${plan.score}/100`
  els.priorityBadge.style.color = priorityColor(plan.score)
  els.planRows.innerHTML = `
    <div class="plan-row"><span>Selected object</span><strong>${escapeHtml(values.selectedObject)}</strong></div>
    <div class="plan-row"><span>Exact Product Token</span><strong>${escapeHtml(values.productToken)}</strong></div>
    <div class="plan-row"><span>System need</span><strong>${escapeHtml(values.systemNeed)}</strong></div>
    <div class="plan-row"><span>Operating units or identities</span><strong>${values.plannedUnits}</strong></div>
    <div class="plan-row"><span>Suggested supply (preset 20% reserve)</span><strong>${plan.productSupply} (${values.plannedUnits} planned + ${plan.reserve} reserve)</strong></div>
    <div class="plan-row"><span>Avatar Coins required</span><strong>${plan.avatarRequired}${values.identityProduct ? ' · one locked per identity' : ' · not an identity product'}</strong></div>
    <div class="plan-row"><span>Weakest factor</span><strong>${escapeHtml(plan.weakestLabel)} · ${plan.weakestValue}</strong></div>
    <div class="plan-row"><span>Suggested next step</span><strong>${escapeHtml(plan.nextAction)}</strong></div>
  `

  drawBarChart(els.factorChart, Object.entries(values.scores).map(([id, value]) => ({ label: factorLabels()[id], value })), 100)
  drawBarChart(els.supplyChart, [
    { label: 'Planned units', value: values.plannedUnits },
    { label: 'Product supply', value: plan.productSupply },
    { label: 'Avatar required', value: plan.avatarRequired },
    { label: 'Contingency', value: plan.reserve }
  ], Math.max(plan.productSupply, 1))
}

function drawBarChart(canvas, rows, maxValue, options = {}) {
  if (!canvas) return
  const context = canvas.getContext('2d')
  const width = canvas.width
  const height = canvas.height
  context.clearRect(0, 0, width, height)
  context.font = options.font || '12px system-ui, sans-serif'
  context.textBaseline = 'middle'
  const left = options.left || 145
  const right = 45
  const top = 15
  const rowHeight = (height - top * 2) / Math.max(rows.length, 1)

  rows.forEach((row, index) => {
    const y = top + index * rowHeight + rowHeight / 2
    const usable = width - left - right
    const ratio = Math.max(0, Math.min(1, row.value / Math.max(maxValue, 1)))
    context.fillStyle = options.textColor || '#8290a8'
    context.fillText(row.label, 6, y)
    context.fillStyle = options.trackColor || 'rgba(120,140,170,.16)'
    context.fillRect(left, y - 8, usable, 16)
    const gradient = context.createLinearGradient(left, 0, left + usable, 0)
    gradient.addColorStop(0, '#4e8dff')
    gradient.addColorStop(1, '#ffe600')
    context.fillStyle = gradient
    context.fillRect(left, y - 8, usable * ratio, 16)
    context.fillStyle = options.valueColor || '#ffffff'
    context.textAlign = 'right'
    context.fillText(String(row.value), width - 5, y)
    context.textAlign = 'left'
  })
}

function drawRankingChart(modules) {
  if (!els.rankingChart) return
  drawBarChart(
    els.rankingChart,
    modules.map(module => ({ label: module.name, value: module.calculatedScore })),
    100,
    { left: 205, textColor: '#afbdd1', valueColor: '#ffffff', trackColor: 'rgba(255,255,255,.08)' }
  )
}

function createVersion(event) {
  event.preventDefault()
  if (!els.tokenForm.reportValidity()) return
  if (![els.creationName, els.productDefinition, els.systemNeed].every(input => input.value.trim())) {
    document.querySelector('#saveStatus').textContent = 'Please add a name, a description, and who it helps.'
    return
  }
  const values = formValues()
  const plan = buildPlan(values)
  const contextId = state.selected?.id || 'unselected'
  const parent = state.local.versions.find(version => version.contextId === contextId)
  const versionNumber = parent ? parent.version + 1 : 1
  const version = {
    id: uid('star'),
    contextId,
    contextType: state.selected?.kind || 'object',
    parentId: parent?.id || null,
    version: versionNumber,
    symbol: '⭐',
    name: `${values.name} Star Blueprint`,
    productToken: values.productToken,
    systemNeed: values.systemNeed,
    plannedUnits: values.plannedUnits,
    identityProduct: values.identityProduct,
    scores: values.scores,
    needScore: plan.score,
    priority: plan.priority,
    productSupply: plan.productSupply,
    avatarRequired: plan.avatarRequired,
    status: 'DRAFT — CAPACITY VERIFICATION REQUIRED',
    createdAt: new Date().toISOString()
  }
  const before = JSON.parse(JSON.stringify(state.local))
  state.local.versions.unshift(version)
  addEvent('STAR_VERSION_CREATED', `${version.name} v${versionNumber} created from ${values.selectedObject}.`, `${plan.score}/100`)
  const status = document.querySelector('#saveStatus')
  try { saveLocal() } catch (_) {
    state.local = before
    status.dataset.error = 'true'
    status.textContent = 'This browser could not save your draft. Your form is still here; storage may be full or blocked.'
    return
  }
  status.dataset.error = 'false'
  status.textContent = `Saved: ${values.name}, version ${versionNumber}. It stays on this browser and has not been minted or published.`
  renderLedger()
  document.querySelector('#ledger').scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function renderLedger() {
  els.versionList.innerHTML = state.local.versions.length
    ? state.local.versions.map(version => `
      <article class="version-card convertible" data-convert-id="${escapeHtml(version.id)}" data-convert-type="blueprint" data-convert-label="${escapeHtml(version.name)}">
        <div class="version-meta"><span>⭐ Version ${version.version}</span><time>${new Date(version.createdAt).toLocaleString()}</time></div>
        <h4>${escapeHtml(version.name)}</h4>
        <p>${escapeHtml(version.productToken)}</p>
        <button type="button" class="button secondary edit-draft" data-version-id="${escapeHtml(version.id)}">Edit this draft</button>
        <div class="version-meta"><span>${escapeHtml(version.priority)} · ${version.needScore}</span><span>Supply ${version.productSupply} · Avatar ${version.avatarRequired}</span></div>
      </article>
    `).join('')
    : '<p class="empty-state">No saved drafts yet. Describe your idea above, then choose Save this draft.</p>'

  els.eventList.innerHTML = state.local.events.length
    ? state.local.events.map(item => `
      <article class="event-card">
        <div class="event-meta"><span>${escapeHtml(item.type)}</span><time>${new Date(item.createdAt).toLocaleString()}</time></div>
        <h4>${escapeHtml(item.amount || 'Ledger event')}</h4>
        <p>${escapeHtml(item.detail)}</p>
      </article>
    `).join('')
    : '<p class="empty-state">The local event ledger is empty.</p>'
  els.versionList.querySelectorAll('[data-version-id]').forEach(button => {
    button.addEventListener('click', () => selectSavedVersion(state.local.versions.find(version => version.id === button.dataset.versionId)))
  })
  markAllConvertible(els.versionList)
}

function resetLedger() {
  if (!window.confirm('Delete all Token Studio drafts saved on this browser? This cannot be undone.')) return
  const before = state.local
  state.local = { schemaVersion: '1.0.0', versions: [], events: [] }
  try { saveLocal() } catch (_) { state.local = before; document.querySelector('#saveStatus').textContent = 'Unable to delete saved drafts: browser storage is blocked.'; return }
  renderLedger()
  document.querySelector('#saveStatus').textContent = 'Saved drafts deleted from this browser.'
}

function bindEvents() {
  document.querySelector('#templateSelect').addEventListener('change', event => {
    if (event.target.value) selectModule(event.target.value)
    else startBlank()
  })
  window.addEventListener('hashchange', revealSection)

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
  els.tokenForm?.addEventListener('submit', createVersion)
  ;[els.creationName, els.productDefinition, els.systemNeed, els.plannedUnits, els.identityProduct]
    .forEach(control => control?.addEventListener(control.type === 'checkbox' ? 'change' : 'input', renderPlan))
  els.resetLedger?.addEventListener('click', resetLedger)
}

async function init() {
  els.year.textContent = new Date().getFullYear()
  bindEvents()
  renderFactorControls()
  markAllConvertible()
  renderLedger()
  startBlank()
  revealSection()

  try {
    state.data = await fetchData()
    renderModules()
    const select = document.querySelector('#templateSelect')
    state.data.modules.forEach(module => {
      const option = document.createElement('option'); option.value = module.id; option.textContent = module.name; select.appendChild(option)
    })
  } catch (error) {
    els.moduleGrid.innerHTML = `<p role="alert">Examples could not load. You can still create your own draft.</p>`
  }
}

function startBlank() {
  state.selected = { kind: 'idea', id: uid('idea'), label: 'My own idea', module: null }
  els.tokenForm.reset()
  els.selectedObject.value = 'My own idea'
  els.factorControls.querySelectorAll('[data-factor]').forEach(input => {
    input.value = 50
    els.factorControls.querySelector(`#output-${CSS.escape(input.dataset.factor)}`).textContent = 50
  })
  document.querySelector('#saveStatus').textContent = 'Nothing saved yet. Review the draft before saving.'
  renderPlan()
}

function selectSavedVersion(version) {
  if (!version) return
  state.selected = { kind: version.contextType, id: version.contextId, label: version.name, module: null }
  document.querySelector('#templateSelect').value = ''
  els.selectedObject.value = `Saved draft: ${version.name} v${version.version}`
  els.creationName.value = version.name.replace(/ Star Blueprint$/, '')
  els.productDefinition.value = version.productToken
  els.systemNeed.value = version.systemNeed
  els.plannedUnits.value = version.plannedUnits
  els.identityProduct.checked = version.identityProduct
  els.factorControls.querySelectorAll('[data-factor]').forEach(input => {
    input.value = version.scores[input.dataset.factor] ?? 50
    els.factorControls.querySelector(`#output-${CSS.escape(input.dataset.factor)}`).textContent = input.value
  })
  renderPlan()
  document.querySelector('#studio').scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function revealSection() {
  const id = window.location.hash.slice(1)
  const target = document.getElementById(id)
  if (!target) return
  let parent = target.parentElement
  while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement }
  target.scrollIntoView({ block: 'start' })
}

init()
