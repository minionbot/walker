# -*- coding: utf-8 -*-
import scrapy
import re
import six
import sys

from tentacle.items import StampGroupCatalogItem, StampSingleCatalogItem, StampGroupCatalog, StampSingleCatalog

class ChinesestampSpider(scrapy.Spider):
    name = 'chinesestamp'
    allowed_domains = ['www.chinesestamp.cn']
    start_urls = [
        'http://chinesestamps.info/c-headed-commemorative-stamps',
        'http://chinesestamps.info/s-headed-special-stamps',
        'http://chinesestamps.info/w-headed-stamps',
        'http://chinesestamps.info/j-headed-commemorative-stamps',
        'http://chinesestamps.info/t-headed-special-stamps',
        'http://chinesestamps.info/stamp-booklet',
        ''
    ]

    def parse(self, response):
        rows = response.css('div#contents div#left_col table tr')
        for row in rows:
            href = row.css('td a::attr(href)').extract_first()
            # yield {'title': row.css('td::text').extract_first().strip()}
            yield scrapy.Request(href, callback = self.parse_stamp_info)

    def parse_stamp_info(self, response):
        name = response.css('div#contents .post_title b::text').extract_first().strip()
        official, name = name.split(' ', 1)

        contents = response.css('div#contents .post_content table tr').extract()
        contents = '\n'.join(contents)
        pub_date, group_num, results, m_info = '', 0, [], None

        if 'J' in official and official != '无编号':
            pub_date, group_num, results = self.parse_j_stamp_content(contents, name.strip(), official)
        elif 'T' in official:
            pub_date, group_num, results = self.parse_t_stamp_content(contents, name.strip(), official)
        elif official.startswith('纪'):
            number = int(official.strip('纪').strip('M').strip())
            if number <= 13:
                return {}
            pub_date, group_num, results = self.parse_c_stamp_content(contents, name.strip(), official)
        elif official.startswith('特'):
            pub_date, group_num, results = self.parse_c_stamp_content(contents, name.strip(), official)
        elif self.is_year_stamp(official):
            pub_date, group_num, results, m_info = self.parse_year_stamp_content(contents, name.strip(), official)
        else:
            raise NotImplementedError('unsupport stamp type')

        image_url = response.css('div#contents .post_content p a::attr(href)').extract_first()
        if image_url is None:
            image_url = response.css('div#contents .post_content p image::attr(href)').extract_first()

        item = StampGroupCatalogItem()
        item['name'] = name.strip()
        item['official'] = official.strip()
        item['group_num'] = group_num
        item['total_face_value'] = 0
        for result in results:
            item['total_face_value'] += int(result.get('face_value', 0))
        item['reference'] = response._get_url()
        item['image_url'] = image_url or ''

        try:
            group = StampGroupCatalog.objects.get(official = official.strip())
        except StampGroupCatalog.DoesNotExist:
            group = item.save()

        for result in results:
            item = StampSingleCatalogItem()
            item['group'] = group
            item['sequence'] = result['sequence']
            item['sequence_name'] = result['sequence_name']
            item['face_value'] = result.get('face_value', 0)
            item['pub_number'] = result.get('pub_number', 0)
            if pub_date:
                item['pub_date'] = pub_date
            try:
                StampSingleCatalog.objects.get(group = group, sequence = int(result['sequence']))
            except StampSingleCatalog.DoesNotExist:
                try:
                    item.save()
                except:
                    """
                    print(
                        'group: %s' % item['group'],
                        'sequence: %s' % item['sequence'],
                        'face_value: %s' % item['face_value'],
                        'pub_number: %s' % result.get('pub_number', 0),
                        contents)"""
                    six.reraise(*sys.exc_info())

        # process M info
        if m_info:
            official = official.strip() + 'M'
            item = StampGroupCatalogItem()
            item['name'] = name.strip()
            item['official'] = official
            item['group_num'] = 1
            item['total_face_value'] = m_info['face_value']
            item['reference'] = response._get_url()
            item['image_url'] = image_url or ''
            try:
                group = StampGroupCatalog.objects.get(official = official)
            except StampGroupCatalog.DoesNotExist:
                group = item.save()

            item = StampSingleCatalogItem()
            item['group'] = group
            item['sequence'] = 1
            item['sequence_name'] = m_info['sequence_name']
            item['face_value'] = m_info.get('face_value', 0)
            item['pub_number'] = m_info.get('pub_number', 0)
            if pub_date:
                item['pub_date'] = pub_date
            try:
                StampSingleCatalog.objects.get(group = group, sequence = 1)
            except StampSingleCatalog.DoesNotExist:
                item.save()

        yield {}
        """
        yield {
            'official': official.strip(),
            'name': name.strip(),
            'image_url': image_url,
            'group_num': group_num,
            'pub_date': pub_date,
            'sequences': results,
            'reference': response._get_url()
        }"""

    def parse_j_stamp_content(self, contents, name, official):

        patterns = [
            r'(\d{1,2})-(\d{1,2}).*?为?.*?[\"“]([^\"”]*)[\"”]',
            r'(\d{1,2})-(\d{1,2})\W+([\u4e00-\u9fa5]+).*\n',
            r'（(\d{1,2})）.*\W+([\u4e00-\u9fa5]+).*\n',
            r'第(\d{1})枚',
            r'共(1)枚.*?',
            r'全套(1)枚',
            r'本套邮票(1)枚'
        ]

        # find publish date
        pub_date = ''
        match = re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', contents)
        if match:
            pub_date = match.group(0)

        for pattern in patterns:
            search = re.compile(pattern)
            matches = search.findall(contents)
            if len(matches):
                break

        if len(matches):
            if len(matches[0]) >= 2:
                results = [{'sequence': match[-2], 'sequence_name': match[-1]} for match in matches]
            elif len(matches[0]) == 1:
                results = [{'sequence': idx, 'sequence_name': name} for idx, match in enumerate(matches)]
        elif 'M' in official:
            results = [{'sequence': 1, 'sequence_name': name}]
        else:
            results = [{'sequence': 1, 'sequence_name': name}]

        return pub_date.replace('.', '-'), len(results), results

    def parse_t_stamp_content(self, contents, name, official):

        def get_match_1(matches):
            return [{
                'sequence': match[0],
                'sequence_name': match[2],
                'face_value': match[1],
                'pub_number': match[3]
            } for match in matches]

        def get_match_2(matches):
            return [{
                'sequence': match[0],
                'sequence_name': match[1],
                'face_value': match[2],
                'pub_number': match[3]
            } for match in matches]

        def get_match_3(matches):
            return [{
                'sequence': match[0],
                'sequence_name': match[2],
                'face_value': match[1].split('+')[0],
                'pub_number': match[3]
            } for match in matches]

        def get_match_4(matches):
            return [{
                'sequence': match[0],
                'sequence_name': match[1],
                'face_value': 0,
                'pub_number': match[2]
            } for match in matches]

        def get_match_5(matches):
            return [{
                'sequence': idx + 1,
                'sequence_name': match[1],
                'face_value': match[0],
                'pub_number': match[2]
            } for idx, match in enumerate(matches)]

        patterns = (
            (r'（(\d{1,3})）\W*?(\d{1,3})[\u4e00-\u9fa5]+\W+([\u4e00-\u9fa5]+)\W+[\D]*?(\d{1,5}(\.\d{1,3})?)',
             get_match_1),
            (r'（(\d{1,3})）\W*?([\u4e00-\u9fa5]+)\W+[\D]*?(\d{1,2})[\u4e00-\u9fa5]+\W+(\d{1,5}(\.\d{1,3})?)',
             get_match_2),
            (r'（(\d{1,3})）\W*?(\d{1}\+\d{1})[\u4e00-\u9fa5]+\W+([\u4e00-\u9fa5]+)\W+[\D]*?(\d{1,5}(\.\d{1,'
             r'3})?)',
             get_match_3
             ),  # 匹配儿童生活
            (r'（\d{1,2}-(\d{1,2})）\W*?[\u4e00-\u9fa5]+\W+([\u4e00-\u9fa5]+)\W+[\D]*?(\d{1,5}(\.\d{1,3})?)',
             get_match_4
             ),
            (r'(\d{1,2})分\W+([\u4e00-\u9fa5]+)\W+[\D]*?(\d{1,5}(\.\d{1,3})?)', get_match_5)
        )

        # find publish date
        pub_date = ''
        match = re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', contents)
        if match:
            pub_date = match.group(0)

        for idx, pattern in enumerate(patterns):
            search = re.compile(pattern[0])
            matches = search.findall(contents)
            if len(matches):
                break

        results = []
        if len(matches):
            results = pattern[1](matches)
        elif 'M' in official:
            results = [{'sequence': 1, 'sequence_name': name}]

        return pub_date.replace('.', '-'), len(results), results

    def parse_c_stamp_content(self, contents, name, official):
        return self.parse_t_stamp_content(contents, name, official)

    def parse_year_stamp_content(self, contents, name, official):

        def get_pattern_1(matches):

            results = []
            for match in matches:
                # normal match
                if len(match) in[5, 6]:
                    if match[0] == '小型张':
                        sequence_num = 'M'
                    else:
                        sequence_num = match[2]
                    sequence_name = match[3]
                    face_value = self.parse_value(match[4])

                    pub_number = 0
                    if len(match) == 6 and pub_number and pub_number != 'M':
                        pub_number = float(match[5])
                else:
                    raise ValueError('Unknown match info')

                results.append({
                    'sequence': sequence_num,
                    'sequence_name': sequence_name,
                    'face_value': face_value,
                    'pub_number': pub_number
                })

            return results

        patterns = (
            (r"([（|(](\d{1,2})-(\d{1,2})[）|)]|小型张)\s*[TJ]?\s*([\u4e00-\u9fa5|\W|\d]+)\s+(\d+\.?\d+\s*[分|元])\s*(\d+.?\d+)?",
             get_pattern_1),
        )

        # find publish date
        pub_date = ''
        match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', contents)
        if match:
            pub_date = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
        else:
            raise ValueError('Can\'t parse any date info.')

        for idx, pattern in enumerate(patterns):
            search = re.compile(pattern[0])
            matches = search.findall(contents)
            if len(matches):
                break

        if len(matches):
            results = pattern[1](matches)
            m_info = None
            for res in results:
                if res['sequence'] == 'M':
                    m_info = res
            if m_info is not None:
                results.remove(m_info)

            return pub_date, len(results), results, m_info
        else:
            raise ValueError('Not match any things.')

    def parse_date(self, contents):
        # find publish date
        pub_date = ''
        match = re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', contents)
        if match:
            pub_date = match.group(0)

        return pub_date

    def is_year_stamp(self, official):
        regex = r"\d{4}-[\u4e00-\u9fa5]?\d{1,2}"
        return re.match(regex, official)

    def parse_value(self, value):
        if '元' in value:
            return int(float(value.strip().strip('元').strip()) * 100)
        elif '分' in value:
            return int(value.strip().strip('分').strip())

        return value
