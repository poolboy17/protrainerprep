import { getPermalink, getBlogPermalink } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Become a Trainer',
      href: getPermalink('/blog/how-to-become-personal-trainer'),
    },
    {
      text: 'Certifications',
      links: [
        {
          text: 'Certification Guide',
          href: getPermalink('/blog/fitness-certification-guide'),
        },
        {
          text: 'NCSF CPT Review',
          href: getPermalink('/blog/ncsf-cpt-review'),
        },
        {
          text: 'NASM vs NCSF',
          href: getPermalink('/blog/nasm-vs-ncsf'),
        },
        {
          text: 'All Cert Reviews',
          href: getPermalink('/category/certifications'),
        },
      ],
    },
    {
      text: 'Career & Money',
      links: [
        {
          text: 'Personal Trainer Salary',
          href: getPermalink('/blog/personal-trainer-salary'),
        },
        {
          text: 'How to Get Clients',
          href: getPermalink('/blog/get-first-10-clients'),
        },
        {
          text: 'All Career Articles',
          href: getPermalink('/category/career'),
        },
      ],
    },
    {
      text: 'Blog',
      href: getBlogPermalink(),
    },
  ],
  actions: [],
};

export const footerData = {
  links: [
    {
      title: 'Guides',
      links: [
        { text: 'Become a Personal Trainer', href: getPermalink('/blog/how-to-become-personal-trainer') },
        { text: 'Certification Guide', href: getPermalink('/blog/fitness-certification-guide') },
        { text: 'Personal Trainer Salary', href: getPermalink('/blog/personal-trainer-salary') },
      ],
    },
    {
      title: 'Certifications',
      links: [
        { text: 'NCSF CPT Review', href: getPermalink('/blog/ncsf-cpt-review') },
        { text: 'NASM vs NCSF', href: getPermalink('/blog/nasm-vs-ncsf') },
        { text: 'Cheapest Certifications', href: getPermalink('/blog/cheapest-personal-trainer-certifications') },
      ],
    },
    {
      title: 'Resources',
      links: [
        { text: 'All Articles', href: getBlogPermalink() },
        { text: 'Career Advice', href: getPermalink('/category/career') },
        { text: 'Business Tips', href: getPermalink('/category/business') },
      ],
    },
    {
      title: 'Legal',
      links: [
        { text: 'Privacy Policy', href: getPermalink('/privacy') },
        { text: 'Terms of Service', href: getPermalink('/terms') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
  ],
  socialLinks: [],
  footNote: `
    © ${new Date().getFullYear()} Pro Trainer Prep · All rights reserved.<br/>
    <span class="text-xs">Affiliate Disclosure: We earn commissions from qualifying purchases at no extra cost to you.</span>
  `,
};
