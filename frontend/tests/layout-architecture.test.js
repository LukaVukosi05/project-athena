const assert=require("assert"),fs=require("fs"),path=require("path");
const root=path.join(__dirname,"..");
const read=name=>fs.readFileSync(path.join(root,name),"utf8");
const pages=["index.html","practice.html","checkout.html","login.html","signup.html","grade.html","topic.html","lesson.html","progress.html","account.html","past-papers.html"];
for(const page of pages){const html=read(page);assert(html.includes('id="nav-mount"'),`${page} must use the shared shell`);assert(html.includes("navigation.js"),`${page} must load shared navigation`);}
assert(read("dashboard.html").includes("url=index.html"));
const tokens=read("css/tokens.css"),components=read("css/components.css"),pageCss=read("css/pages.css");
for(const token of ["--athena-navy: #18324a","--athena-teal: #167d87","--athena-gold: #d7a62c","--athena-background: #f5f8fa"]){assert(tokens.includes(token));}
assert(components.includes("min-height:44px"));
assert(components.includes(".nav-menu-toggle")&&components.includes("@media (max-width: 860px)"));
assert(pageCss.includes("@media(max-width:720px)")&&pageCss.includes(".lesson-layout"));
const landing=read("index.html");assert(landing.includes("Understand every step. Recover every mark."));assert(landing.includes("CAPS-aligned Mathematics for Grades 8–12"));
for(const principle of ["See every step","Fix the first mistake","Track real improvement"])assert(landing.includes(principle));
assert(landing.includes("Choose your grade")&&landing.includes("Inside every usable lesson"));
const landingSource=read("js/pages/landing.js");
assert(landingSource.includes('fetch(url)')&&landingSource.includes('url="/api/v1/curriculum/grades"'));
assert(!landingSource.includes("/api/v1/curriculum/grades/grade-12"));
const account=read("account.html");assert(account.includes("14-day free trial"));assert(account.includes("Payment details required"));assert(account.includes("R149"));assert(account.includes('href="checkout.html"'));
const progress=read("progress.html");assert(progress.includes("Not enough evidence"));assert(!progress.match(/\b[1-9]\d?% readiness/i));
const grade=read("grade.html");for(let n=8;n<=12;n++)assert(grade.includes(`grade-${n}`));
const topic=read("js/pages/topic.js");assert(topic.includes('lesson.readiness === "published"'));assert(topic.includes("Boolean(lesson.usable)"));
const lesson=read("lesson.html");assert(lesson.includes("lesson-stage-nav")&&lesson.includes("lesson-support"));
console.log("responsive application architecture contract passed");
