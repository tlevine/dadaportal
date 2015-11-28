from nikola.plugin_categories import Task
from nikola import utils

from .big import guess_slides

class Slides(Task):
    'Render posts as slides.'
    name = 'big'
    def gen_tasks(self):
        pass

    def set_site(self, site):
        """Set Nikola site."""
        site.register_path_handler('slides', self.slides_path)
        return super(Slides, self).set_site(site)

    def _prepare_task(self, kw, name, lang, posts, items, template_name,
                      title, deps_translatable=None):
        """Prepare an archive task."""
        # name: used to build permalink and destination
        # posts, items: posts or items; only one of them should be used,
        #               the other should be None
        # template_name: name of the template to use
        # title: the (translated) title for the generated page
        # deps_translatable: dependencies (None if not added)
        assert posts is not None or items is not None
        task_cfg = [copy.copy(kw)]
        context = {}
        context["lang"] = lang
        context["title"] = title
        context["permalink"] = self.site.link("archive", name, lang)
        context["pagekind"] = ["list", "archive_page"]
        if posts is not None:
            context["posts"] = posts
            # Depend on all post metadata because it can be used in templates (Issue #1931)
            task_cfg.append([repr(p) for p in posts])
        else:
            # Depend on the content of items, to rebuild if links change (Issue #1931)
            context["items"] = items
            task_cfg.append(items)
        task = self.site.generic_post_list_renderer(
            lang,
            [],
            os.path.join(kw['output_folder'], self.site.path("archive", name, lang)),
            template_name,
            kw['filters'],
            context,
        )

        task_cfg = {i: x for i, x in enumerate(task_cfg)}
        if deps_translatable is not None:
            task_cfg[3] = deps_translatable
        task['uptodate'] = task['uptodate'] + [config_changed(task_cfg, 'nikola.plugins.task.archive')]
        task['basename'] = self.name
        return task

    def _generate_posts_task(self, kw, name, lang, posts, title, deps_translatable=None):
        """Genereate a task for an archive with posts."""
        posts = sorted(posts, key=lambda a: a.date)
        posts.reverse()
        if kw['archives_are_indexes']:
            def page_link(i, displayed_i, num_pages, force_addition, extension=None):
                feed = "_atom" if extension == ".atom" else ""
                return adjust_name_for_index_link(self.site.link("archive" + feed, name, lang), i, displayed_i,
                                                  lang, self.site, force_addition, extension)

            def page_path(i, displayed_i, num_pages, force_addition, extension=None):
                feed = "_atom" if extension == ".atom" else ""
                return adjust_name_for_index_path(self.site.path("archive" + feed, name, lang), i, displayed_i,
                                                  lang, self.site, force_addition, extension)

            uptodate = []
            if deps_translatable is not None:
                uptodate += [config_changed(deps_translatable, 'nikola.plugins.task.archive')]
            context = {"archive_name": name,
                       "is_feed_stale": kw["is_feed_stale"],
                       "pagekind": ["index", "archive_page"]}
            yield self.site.generic_index_renderer(
                lang,
                posts,
                title,
                "archiveindex.tmpl",
                context,
                kw,
                str(self.name),
                page_link,
                page_path,
                uptodate)
        else:
            yield self._prepare_task(kw, name, lang, posts, None, "list_post.tmpl", title, deps_translatable)

    def gen_tasks(self):
        """Generate archive tasks."""
        kw = {
            "messages": self.site.MESSAGES,
            "translations": self.site.config['TRANSLATIONS'],
            "output_folder": self.site.config['OUTPUT_FOLDER'],
            "filters": self.site.config['FILTERS'],
            "show_untranslated_posts": self.site.config['SHOW_UNTRANSLATED_POSTS'],
            "pretty_urls": self.site.config['PRETTY_URLS'],
            "strip_indexes": self.site.config['STRIP_INDEXES'],
            "index_file": self.site.config['INDEX_FILE'],
        }
        self.site.scan_posts()
        yield self.group_task()
        for lang in kw["translations"]:
            for year, posts in archdata.items():
                # Filter untranslated posts (Issue #1360)
                if not kw["show_untranslated_posts"]:
                    posts = [p for p in posts if lang in p.translated_to]

                # Add archive per year or total archive
                if year:
                    title = kw["messages"][lang]["Posts for year %s"] % year
                    kw["is_feed_stale"] = (datetime.datetime.utcnow().strftime("%Y") != year)
                else:
                    title = kw["messages"][lang]["Archive"]
                    kw["is_feed_stale"] = False
                deps_translatable = {}
                for k in self.site._GLOBAL_CONTEXT_TRANSLATABLE:
                    deps_translatable[k] = self.site.GLOBAL_CONTEXT[k](lang)
                if not kw["create_monthly_archive"] or kw["create_full_archives"]:
                    yield self._generate_posts_task(kw, year, lang, posts, title, deps_translatable)
                else:
                    months = set([(m.split('/')[1], self.site.link("archive", m, lang), len(self.site.posts_per_month[m])) for m in self.site.posts_per_month.keys() if m.startswith(str(year))])
                    months = sorted(list(months))
                    months.reverse()
                    items = [[nikola.utils.LocaleBorg().get_month_name(int(month), lang), link, count] for month, link, count in months]
                    yield self._prepare_task(kw, year, lang, None, items, "list.tmpl", title, deps_translatable)

        if not kw['create_single_archive'] and not kw['create_full_archives']:
            # And an "all your years" page for yearly and monthly archives
            if "is_feed_stale" in kw:
                del kw["is_feed_stale"]
            years = list(self.site.posts_per_year.keys())
            years.sort(reverse=True)
            kw['years'] = years
            for lang in kw["translations"]:
                items = [(y, self.site.link("archive", y, lang), len(self.site.posts_per_year[y])) for y in years]
                yield self._prepare_task(kw, None, lang, None, items, "list.tmpl", kw["messages"][lang]["Archive"])

    def archive_path(self, name, lang, is_feed=False):
        """Link to archive path, name is the year.

        Example:

        link://archive/2013 => /archives/2013/index.html
        """
        archive_file = self.site.config['ARCHIVE_FILENAME']
        index_file = self.site.config['INDEX_FILE']
        if name:
            return [_f for _f in [self.site.config['TRANSLATIONS'][lang],
                                  self.site.config['ARCHIVE_PATH'], name,
                                  index_file] if _f]
        else:
            return [_f for _f in [self.site.config['TRANSLATIONS'][lang],
                                  self.site.config['ARCHIVE_PATH'],
                                  archive_file] if _f]
