    name = 'Git'

                                 'HEAD'], ignore_errors=True).strip()
        if self.head_ref:
            short_head = self._strip_heads_prefix(self.head_ref)
            merge = execute([self.git, 'config', '--get',
                             'branch.%s.merge' % short_head],
                            ignore_errors=True).strip()
            remote = execute([self.git, 'config', '--get',
                              'branch.%s.remote' % short_head],
                             ignore_errors=True).strip()

            merge = self._strip_heads_prefix(merge)
            if remote and remote != '.' and merge:
                self.upstream_branch = '%s/%s' % (remote, merge)
        head_ref = "HEAD"
        if self.head_ref:
            head_ref = self.head_ref
                                   head_ref]).strip()
            diff_lines = self.make_diff(self.merge_base, head_ref)
            cmdline = [self.git, "diff", "--no-color", "--full-index",
                       "--no-ext-diff", "--ignore-submodules", "--no-renames",
                       rev_range]

            if (self.server and
                self.server.capabilities.has_capability('diffs',
                                                        'moved_files')):
                cmdline.append('-M')

            return execute(cmdline)
        head_ref = "HEAD"
        if self.head_ref:
            head_ref = self.head_ref

                                   head_ref]).strip()