const heroForm=document.querySelector('#infinitySearch');
const heroSearch=document.querySelector('#heroSearch');
const resultTitle=document.querySelector('#resultTitle');
const resultText=document.querySelector('#resultText');

heroForm.addEventListener('submit',event=>{
  event.preventDefault();
  const query=heroSearch.value.trim();
  if(!query){
    heroSearch.focus();
    resultTitle.textContent='What should Infinity find?';
    resultText.textContent='Enter a project, tool, or idea to begin the extraction.';
    return;
  }
  const words=query.toLowerCase().split(/\s+/);
  const matches=repos.filter(repo=>{
    const haystack=`${repo.name} ${repo.description||''}`.toLowerCase();
    return words.every(word=>haystack.includes(word));
  });
  search.value=query;
  category='All';
  filters.querySelectorAll('button').forEach(button=>button.classList.toggle('active',button.dataset.category==='All'));
  render();
  resultTitle.textContent=matches.length?`${matches.length} connected ${matches.length===1?'result':'results'} found`:'No exact repository match yet';
  resultText.textContent=matches.length?`Blue transfer is holding the strongest matches for “${query}”. Open the project directory below to choose one.`:`“${query}” was indexed and extracted. Try a broader project, tool, science, media, game, wallet, or token term.`;
  if(matches.length)document.querySelector('#projects').scrollIntoView({behavior:'smooth',block:'start'});
});
