/** @type {import('shared-test-utils').SiteConfig} */
export default {
  siteName: 'ProTrainerPrep',
  distDir: './dist',

  // Blog posts are nested: dist/category-name/slug/index.html
  // Match anything that looks like category/slug (two levels deep).
  // Also match top-level content pages (privacy, terms, etc.).
  pagePattern: /^.+$/,

  // Use recursive discovery to find nested blog posts
  discoverOpts: { recursive: true },

  // Directories to skip
  excludeDirs: ['_astro', 'rss.xml', 'tag', '404.html'],

  checks: {
    duplicateIds: true,
    headingHierarchy: true,
    headTags: {
      requireCanonical: true,
      requireOgImage: true,
      requireDescription: true,
    },
  },
};
