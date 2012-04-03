import sublime, sublime_plugin, commands, re

class PhpBuildCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		(return_code, output) = commands.getstatusoutput("php -l '%s'" % view.file_name())
		op = self.window.get_output_panel('php_build')
		op.set_read_only(False)
		edit = op.begin_edit()
		region = sublime.Region(0, op.size())
		op.erase(edit, region)
		op.insert(edit, 0, output)
		op.end_edit(edit)
		op.set_read_only(True)
		self.window.run_command("show_panel", {"panel": "output.php_build"})

		if (return_code != 0):
			m = re.search('on line ([0-9]+)', output)
			if (m.groups() > 0):
				p = view.text_point(int(m.groups()[0]) - 1, 0)
				view.sel().clear()
				view.sel().add(sublime.Region(p, p))

