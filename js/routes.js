var pages = {
	"/" : "./templates/home",
	"/about" : "./templates/experience",
	"/experience" : "./templates/experience",
	"/projects" : "./templates/projects",
	"/education" : "./templates/education",
	"/blog" : "./templates/blog",
	"/contact" : "./templates/contact"
};

pages.render = function (path) {
	var path = path.path;
	var fn = jade.compileFile(pages[path]);
	console.log(fn);
	console.log(path)
	// render template
}

page.base('/ncsu/portfolio')
page('/', pages.render);
page('/about', pages.render);
page('/experience', pages.render);
page('/projects', pages.render);
page('/education', pages.render);
page('/blog', pages.render);
page('/contact', pages.render)
page();