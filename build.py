# coding: utf-8
from pathlib import Path
from html import escape as esc
import hashlib
import json
import re
ROOT=Path(__file__).parent
D=json.loads((ROOT/'content.json').read_text())
def e(x): return esc(str(x),quote=True)
def lead_text(x):
 def group(match): return '<span class="nowrap">'+match.group(0).replace('·','&nbsp;·&nbsp;')+'</span>'
 return re.sub(r'[^\s<>]+(?:·[^\s<>]+)+',group,e(x))
def links(xs): return ''.join(f'<a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["title"])}</a>' for x in xs)
def flow(xs): return '<ol class="flow">'+''.join(f'<li><span>{e(x)}</span></li>' for x in xs)+'</ol>'
def gallery(key):
 if key in ('tk8','tk8-features'):
  items=[('characters','캐릭터 탐색'),('moves','기술 목록'),('search','기술 검색')] if key=='tk8' else [('video','기술 영상 재생'),('memo','캐릭터별 메모')]
  return '<figure class="gallery"><div class="screens tk8 direct">'+''.join(f'<div class="screen-item"><a class="screen" href="assets/tk8-{cl}.png" target="_blank" rel="noopener" aria-label="{e(cap)} 화면 원본 보기"><img src="assets/tk8-{cl}.png" alt="{e(cap)} 화면" loading="lazy"></a><p>{e(cap)}</p></div>' for cl,cap in items)+'</div><figcaption>직접 제공한 개발 화면 · 이미지를 누르면 원본을 볼 수 있습니다.</figcaption></figure>'
 else:
  items=[('journals','회고 목록'),('chat','대화형 회고')];file='retstalk-preview.png'
 return '<figure class="gallery"><div class="screens '+key+'">'+''.join(f'<div class="screen-item"><div class="screen {cl}"><img src="assets/{file}" alt="{e(cap)} 화면" loading="lazy"></div><p>{e(cap)}</p></div>' for cl,cap in items)+'</div><figcaption>프로젝트 README에 보존된 당시 서비스 화면</figcaption></figure>'
def case(c,idx,first=False):
 met=c.get('metric');m=''
 if met:m=f'<div class="comparison"><div><span>변경 전</span><strong>{e(met["before"])}</strong></div><div><span>변경 후</span><strong>{e(met["after"])}</strong></div><p>{e(met["label"])}</p></div><p class="note">{e(met["note"])}</p>'
 f=flow(c['flow']) if c.get('flow') else ''
 note=f'<p class="note">{e(c["note"])}</p>' if c.get('note') else ''
 return f'''<details class="case" {'open' if first else ''}><summary><span class="case-index">{idx:02}</span><span><span class="case-label">{e(c['label'])}</span><h3>{e(c['title'])}</h3></span><span class="toggle" aria-hidden="true"></span></summary><div class="case-body"><p class="problem">{e(c['problem'])}</p>{f}<div class="case-columns"><div><h4>제가 한 작업</h4><ul>{''.join('<li>'+e(s)+'</li>' for s in c['actions'])}</ul></div><div class="outcome"><h4>달라진 점</h4><p>{e(c['result'])}</p></div></div>{m}{note}</div></details>'''
def project(p):
 num=p['number'];meta=f'{p["subtitle"]} · {p["period"]}'
 l=f'<div class="links">{links(p.get("links",[]))}</div>' if p.get('links') else ''
 status=f'<p class="status">{e(p["status"])}</p>' if p.get('status') else ''
 metrics=''
 if p.get('metrics'):metrics='<div class="metrics">'+''.join(f'<div class="metric"><strong>{e(x["value"])}</strong><span>{e(x["label"])}</span><small>{e(x.get("note",""))}</small></div>' for x in p['metrics'])+'</div>'
 media=gallery(p['gallery']) if p.get('gallery') else ''
 if p['id']=='todakun':media='<figure class="todakun-intro"><a href="assets/todakun-introduction.png" target="_blank" rel="noopener" aria-label="토닥운 소개 이미지 원본 보기"><img src="assets/todakun-introduction.png" alt="토닥운 팀 소개 이미지: 대화하는 AI 사주 서비스와 대표 화면" loading="lazy"></a><figcaption>팀에서 제작한 서비스 소개 이미지</figcaption></figure><details class="poster-details"><summary>서비스 소개 이미지 전체 보기</summary><img src="assets/todakun-introduction.png" alt="토닥운 서비스 배경, 오늘의 운세 리포트, AI 채팅 및 행운 액션 소개" loading="lazy"></details>'
 if p.get('overviewFlow'):media+='<div class="overview-flow"><p class="eyebrow">'+('CHAT DATA FLOW' if p['id']=='todakun' else 'AUDIO CONVERSATION')+'</p>'+flow(p['overviewFlow'])+'</div>'
 header=f'''<div class="project-top"><div><div class="project-number">{num} · {e(p['kind'])}</div><h2>{e(p['name'])}</h2><p class="subhead">{e(meta)}</p><p class="project-scope">{e(p['scope'])}</p></div>{l}</div>'''
 tags='<div class="tags">'+''.join(f'<span class="tag">{e(t)}</span>' for t in p['tech'])+'</div>'
 roles='<div class="role-list"><h4>담당 범위</h4><ul>'+''.join('<li>'+e(s)+'</li>' for s in p['roles'])+'</ul></div>'
 reflection_parts=[s for s in p.get('reflection','').split('\n\n') if s.strip()]
 print_reflection=''.join('<p>'+('<b>이 경험에서 남은 점 · </b>' if i==0 else '')+e(s)+'</p>' for i,s in enumerate(reflection_parts))
 print_extras='<div class="print-only">'+''.join(f'<p><b>{e(x["title"])} · </b>{e(x["text"])}</p>' for x in p.get('additional',[]))+print_reflection+'</div>'
 overview=f'<div class="print-page project-overview">{header}<p class="lead">{lead_text(p["description"])}</p>{tags}{roles}{status}{metrics}{media}{print_extras}</div>'
 groups=''
 cs=p.get('cases',[])
 for i in range(0,len(cs),2):
  cases=''.join(case(c,i+j+1,first=(i+j==0)) for j,c in enumerate(cs[i:i+2]))
  groups+=f'<div class="print-page case-group"><div class="print-chapter">{num} · {e(p["name"])} / 주요 사례</div>{cases}</div>'
 additional=''
 if p.get('additional'):additional='<div class="additional"><h4>함께 구현한 기능</h4>'+''.join(f'<div><b>{e(x["title"])}</b><p>{e(x["text"])}</p></div>' for x in p['additional'])+'</div>'
 reflection='<div class="reflection"><span>이 경험에서 남은 점</span><div>'+''.join('<p>'+e(s)+'</p>' for s in reflection_parts)+'</div></div>' if reflection_parts else ''
 feature_media='<section class="print-page feature-gallery"><div class="project-number">'+num+' · 격투 게임 정보 앱</div><h3>영상으로 확인하고, 메모로 기록하기</h3><p>기술 상세 화면에서 동작 영상을 확인하고, 캐릭터별 메모로 학습 내용을 기록합니다.</p>'+gallery('tk8-features')+'</section>' if p['id']=='tk8' else ''
 return f'<article id="{p["id"]}" class="project {p["id"]}"><div class="wrap">{overview}{groups}{feature_media}<div class="project-ending">{additional}{reflection}</div></div></article>'
nav=''.join(f'<a href="#{x["id"]}">{e(x["name"] if x["id"] in ["tk8","todakun","retstalk"] else "인턴" if x["id"]=="intern" else "Comi")}</a>' for x in D['projects'])
toc='<div class="print-toc"><h3>프로젝트</h3>'+''.join(f'<a href="#{p["id"]}"><b>{p["number"]} · {e(p["name"])}</b><span>{e(p["scope"])}</span></a>' for p in D['projects'])+'</div>'
style_hash=hashlib.sha256((ROOT/'dist/style.css').read_bytes()).hexdigest()[:12]
html=f'''<!doctype html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>문영균 · iOS 개발 포트폴리오</title><meta name="description" content="문영균의 iOS 개발 포트폴리오. 앱 출시와 운영, 비동기 데이터 처리, 팀 개발과 AI 보조 검토 경험."><link rel="stylesheet" href="style.css?v={style_hash}"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23112039'/%3E%3Cpath d='M8 23V9l8 9 8-9v14' fill='none' stroke='white' stroke-width='3'/%3E%3C/svg%3E"></head><body><a class="skip" href="#main">본문으로 이동</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="#main"><span class="mark">MG</span>문영균 · iOS</a><nav class="nav" aria-label="프로젝트">{nav}</nav></div></header><main id="main"><section class="hero wrap print-page"><div class="eyebrow">PORTFOLIO · 2026</div><h1>문영균,<br>iOS 개발자</h1><div class="hero-row"><div><p>{e(D['intro'])}</p><div class="contact"><a href="mailto:{D['email']}">{e(D['email'])}</a><a href="{D['github']}" target="_blank" rel="noopener">GitHub</a><a class="pdf-download" href="portfolio.pdf" download="문영균_포트폴리오_초안.pdf">PDF 다운로드</a></div></div><aside class="hero-aside" aria-label="경험 요약"><div><b>출시와 운영</b><span>개인 iOS 앱</span></div><div><b>비동기 데이터</b><span>채팅 · 캐싱 · 동기화</span></div><div><b>AI 활용과 검토</b><span>기능 구현 · 운영 도구</span></div></aside></div>{toc}</section>{''.join(project(p) for p in D['projects'])}<section class="background wrap print-page"><div class="project-number">BACKGROUND</div><h2>학습과 경력의 기반</h2><div class="background-grid"><div><h3>교육</h3><ul>{''.join('<li>'+e(x)+'</li>' for x in D['education'])}</ul></div><div><h3>자격 · 어학</h3><ul>{''.join('<li>'+e(x)+'</li>' for x in D['certifications'])}</ul></div></div><div class="contact"><a href="mailto:{D['email']}">{e(D['email'])}</a><a href="{D['github']}" target="_blank" rel="noopener">GitHub · MoonGoon72</a></div></section></main><footer><div class="wrap footer-inner"><span>문영균 · iOS Developer</span><span>{e(D['updated'])} · Portfolio draft</span></div></footer><script src="main.js"></script></body></html>'''
(ROOT/'dist/index.html').write_text(html)
# Editable candidate-facing prose, generated from the same content used by the website.
md=[f'# {D["name"]} | {D["role"]}',D['intro'],f'{D["email"]} · {D["github"]}']
for p in D['projects']:
 md.extend([f'## {p["name"]}',f'{p["subtitle"]} | {p["period"]} | {p["scope"]}',p['description']])
 if p.get('status'):md.append(p['status'])
 md.append('### 담당 범위');md.extend('- '+s for s in p['roles'])
 for c in p.get('cases',[]):
  md.extend(['### '+c['title'],c['problem']]);md.extend('- '+s for s in c['actions']);md.append('결과: '+c['result'])
  if c.get('metric'):md.extend([c['metric']['before']+' → '+c['metric']['after'],c['metric']['note']])
  if c.get('note'):md.append(c['note'])
 for x in p.get('additional',[]):md.extend(['### '+x['title'],x['text']])
 if p.get('reflection'):md.append('이 경험에서 남은 점: '+p['reflection'])
(ROOT/'portfolio-copy.md').write_text('\n\n'.join(md)+'\n')
print(f'Built {len(D["projects"])} projects and {sum(len(p["cases"]) for p in D["projects"])} case studies')
