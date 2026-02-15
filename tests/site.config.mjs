/** @type {import('shared-test-utils').SiteConfig} */
export default {
  siteName: 'ProTrainerPrep',
  distDir: './dist',

  // Blog posts live under /[...blog]/ — match any folder in dist/
  // that looks like a blog slug (lowercase words with hyphens).
  // Excludes top-level static pages (index, 404, privacy, etc.)
  pagePattern: /^[a-z][a-z0-9-]+[a-z0-9]$/,

  // Directories to skip when scanning dist/
  excludeDirs: ['_astro', 'rss.xml', 'category', 'tag'],

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
