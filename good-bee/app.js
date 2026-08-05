const state = { data: null }

const els = {
  menuButton: document.querySelector('#menuButton'),
  mainNav: document.querySelector('#mainNav'),
  form: document.querySelector('#packageForm'),
  planType: document.querySelector('#planType'),
  environment: document.querySelector('#environment'),
  stayLength: document.querySelector('#stayLength'),
  accessNotes: document.querySelector('#accessNotes'),
  packageTitle: document.querySelector('#packageTitle'),
  packageSummary: document.querySelector('#packageSummary'),
  packageContents: document.querySelector('#packageContents'),
  homeGrid: document.querySelector('#homeGrid'),
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
  const response = await fetch('./data/programs.json', { headers: { Accept: 'application/json' } })
  if (!response.ok) throw new Error(`Program data unavailable (${response.status})`)
  return response.json()
}

function renderHomes(homes = []) {
  els.homeGrid.innerHTML = homes.map((home, index) => `
    <article class="home-card">
      <span class="home-number">${String(index + 1).padStart(2, '0')}</span>
      <span class="type">${escapeHtml(home.type)}</span>
      <h3>${escapeHtml(home.name)}</h3>
      <p>${escapeHtml(home.summary)}</p>
      <p><strong>Assembly:</strong> ${escapeHtml(home.assembly)}</p>
      <div class="feature-tags">
        ${home.features.map(feature => `<span>${escapeHtml(feature)}</span>`).join('')}
      </div>
    </article>
  `).join('')
}

function chosenSupports() {
  return [...els.form.querySelectorAll('input[name="support"]:checked')]
    .map(input => input.value)
}

function readableSupport(value) {
  const labels = {
    'accessible-transport': 'Accessible transportation',
    'daily-checkin': 'Daily check-in',
    'personal-assistance': 'Personal assistance',
    nursing: 'Nursing coordination',
    meal: 'Meals or groceries',
    companion: 'Chosen companion'
  }
  return labels[value] || value
}

function selectProgram(planType, environment) {
  const programs = state.data?.destinations || []
  if (planType === 'move') {
    if (environment === 'mountain') return programs.find(item => item.id === 'mountain-move')
    return programs.find(item => item.id === 'coastal-move')
  }
  if (environment === 'mountain') return programs.find(item => item.id === 'mountain-renewal')
  if (environment === 'travel') return programs.find(item => item.id === 'sail-and-see')
  return programs.find(item => item.id === 'florida-coast')
}

function buildUnits(program, days, supports) {
  const units = []
  const base = program?.tokens || {}

  if (base.night) units.push({ label: 'Stay nights', value: Math.min(days, base.night) })
  if (base.ride) units.push({ label: 'Accessible rides', value: base.ride + (days >= 30 ? 4 : 0) })
  if (base.meal || supports.includes('meal')) units.push({ label: 'Meals or grocery units', value: Math.max(base.meal || 0, days) })
  if (base.supportHour || supports.some(value => ['daily-checkin', 'personal-assistance', 'nursing'].includes(value))) {
    const requested = supports.includes('personal-assistance') ? days * 2 : supports.includes('daily-checkin') ? Math.ceil(days / 2) : 0
    units.push({ label: 'Support coordination hours', value: Math.max(base.supportHour || 0, requested) })
  }
  if (base.experience) units.push({ label: 'Adaptive experiences', value: base.experience })
  if (base.movePackage) units.push({ label: 'Defined move package', value: base.movePackage })
  if (base.homeSetup) units.push({ label: 'Home setup package', value: base.homeSetup })

  return units
}

function buildPackage(event) {
  event.preventDefault()
  if (!state.data) return

  const planType = els.planType.value
  const environment = els.environment.value
  const days = Number(els.stayLength.value)
  const supports = chosenSupports()
  const notes = els.accessNotes.value.trim()
  const program = selectProgram(planType, environment === 'open' ? 'beach' : environment)

  if (planType === 'home') {
    els.packageTitle.textContent = 'Accessible home discovery package'
    els.packageSummary.textContent = 'Compare private home models, choose an environment, document access requirements, inspect local services, and approve a site only after the resident reviews the complete plan.'
  } else {
    els.packageTitle.textContent = program?.name || 'Good Bee person-directed package'
    els.packageSummary.textContent = program?.summary || 'A voluntary package assembled around the person’s stated destination and support choices.'
  }

  const items = [
    { label: 'Plan', value: els.planType.options[els.planType.selectedIndex].text },
    { label: 'Environment', value: els.environment.options[els.environment.selectedIndex].text },
    { label: 'Initial period', value: planType === 'move' ? '90-day transition review' : `${days} days` },
    { label: 'Support choices', value: supports.length ? supports.map(readableSupport).join(', ') : 'No additional support selected' },
    { label: 'Accessibility', value: notes || 'To be completed privately with the resident' },
    { label: 'Exit protection', value: planType === 'move' ? 'Transition, dispute, and recovery plan required' : 'Return travel reserved before departure' }
  ]

  const units = planType === 'home'
    ? [
        { label: 'Site and access review', value: 1 },
        { label: 'Home configuration', value: 1 },
        { label: 'Licensed plan review', value: 1 },
        { label: 'Resident approval checkpoints', value: 4 }
      ]
    : buildUnits(program, days, supports)

  els.packageContents.innerHTML = `
    ${items.map(item => `
      <article class="package-item">
        <strong>${escapeHtml(item.label)}</strong>
        <span>${escapeHtml(item.value)}</span>
      </article>
    `).join('')}
    ${units.map(unit => `
      <article class="package-item">
        <strong>${escapeHtml(unit.label)}</strong>
        <span>${escapeHtml(unit.value)} example benefit unit${unit.value === 1 ? '' : 's'}</span>
      </article>
    `).join('')}
  `

  // Accessibility notes can be sensitive. This front-end prototype deliberately
  // displays them only in the current page and never stores them in localStorage.
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

async function init() {
  bindNavigation()
  els.form?.addEventListener('submit', buildPackage)
  els.year.textContent = new Date().getFullYear()

  try {
    state.data = await fetchData()
    renderHomes(state.data.homes)
  } catch (error) {
    els.homeGrid.innerHTML = `<p role="alert">${escapeHtml(error.message)}</p>`
  }
}

init()
