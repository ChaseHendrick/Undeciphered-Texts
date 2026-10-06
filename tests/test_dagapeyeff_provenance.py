"""The cells and the scores that depend on them hash to a fixed chain."""

from __future__ import annotations

import time
import unittest

from engine.dagapeyeff_provenance import provenance_report


class DagapeyeffProvenanceTest(unittest.TestCase):
    def test_the_chain_reads_the_frozen_scores(self) -> None:
        started = time.perf_counter()
        report = provenance_report()
        self.assertLess(time.perf_counter() - started, 15)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(
            [(entry["name"], entry["content_sha256"]) for entry in report["entries"]],
            [
                ("cells", "f2460a6acdf2f50e12fdc8760c39753746d885282cd0bdfd0eec877c56e6fae5"),
                ("yardstick", "e12910ac3d3d0460db9ce76719298d94f261b7a8a17f09fec675dc4cda635d66"),
                ("balls", "3b84e9af30916cf42181a75d847eff6ba0cc992f606a069fe8fcfc5af0227bdd"),
                ("record", "834058b318779e3811b0b19408329f702bbf3577623dc17912af55c62efc80f7"),
                ("convert", "a64782364904d7e20b9436212d93d90caa172f851d0b0442045943a013c9e549"),
                ("edits", "f662992893d0108c125b14cac1d20a30f7eafe2c58bf6bcc54e9dbc8b5744688"),
                ("corrections", "bf4a749875d9bbd6d318016e7b2a390778d0854257a2e2bb59c3f6acf524d929"),
                ("regroup", "56066cbfba47752377e800bb6816c837c2745467c1a47774fcb162a303a62309"),
                ("keys", "3fe9d3522a1017aa1348f5fa0dd561ccf8940a1bbff5fe6e8246a180c093ae37"),
                ("model", "0d050d25e8e1d2287335f78b6a8e891c0a10a751e9eaa5b7de93bdf7b1e52cf8"),
                ("bifid", "eb196ec222b01a977c3e0694b371af2c97ebae5d6f322aad5e9ddb80804b5c68"),
                ("period4", "932ab042c00b4245c0e68bae71285878574320125580b83ca6e20fee1b48160f"),
                ("word", "ccf44aceb6efea160894fa3730d3cf0e999d5eccdeeebb447e41983867ae8b36"),
                ("running", "1b8674ddd9b6bcb520613739a11188ad3bc623973d24ee603b73b8078d423f33"),
                ("patterns", "c5a700688728c2b918a8c3835ad66f3fc95631500091b122153fc599432a6365"),
                ("columns", "545dc79eab57e4d8457943ca70b90d303b2a3533500f8558aca5b70605aa2492"),
                ("board", "3b39a845596491cb92c951d67d82ce49e5773379c082cc005c978c2a80b527a9"),
                ("infer", "c67768bd2e358814d7b1faea635b909637f2eb2ca249c6053f6889e958c409c0"),
                ("foresight", "48ceb2bf1c6010816c96eb483fccd9dc5609748da14cb459b638f94f94a29e10"),
                ("checks", "cdf3738a31095c2bee1ab125adeab35331909b362801882d5285e373ee3b41ea"),
                ("adversary", "27532401beeff15910f3beb80b6bef2095313b8beb709213f46ee2ce8adede86"),
                ("autokey", "291d0e3ead0bb0903b5a93f7851c44dc9f491060cc3a62a8302759af2a863306"),
                ("digit-routes", "97547066e834b8423c9edee4d893b838baa6b8a22d530d821c0eb2306f1577af"),
                ("angles", "b8a3311101662a1c4d86365b052271bc112878168f513353cbd4845112e061d0"),
                ("delay", "56016bdaf30c3aef8ebcfb956b21a3af8605b88d526667a439d5d476a4765380"),
                ("bookkey", "d62759d707cb9782bc9c138e110b0bbea61d02b7052071be4c4d1e0ff3563184"),
                ("groups", "f80567663cc41f4175fdaa88a8b5fab1306c4bc97069bdc2f158b522c077b1ac"),
                ("places", "142b6e3498c975797e9b5d80f5f3c534e1cbd06a217dc90054d177da2297dfaf"),
                ("solver-swarm", "21509a963f29551ce6155319f60d82e64d1da3d2acbe267c1a4201472779330e"),
                ("classic-swarm", "396a9fa86092731be302bb8243d61f48adde06a54d61dbf8d325d5664c63cfcf"),
                ("router-swarm", "d6539df9419052f5d7137974173ac4d55f5110bea168ddface2c716d84af27a6"),
                ("column-null", "7c9bc0e57380cd289805fe8fc7197982a806d38ab99c4bc74791fa4f7d47a5ac"),
                ("large-swarm", "3cb01d80cd5b96ce4f12e3e08a9c646626159e91ce0f7480e6cf48cff174c327"),
                ("refined-swarm", "b20eb44ed7d876ec239be0dc6df48650350dd6de9d6f4a83516b48bbe3f8c9a4"),
                ("bob-caution", "65aa758f96e16ee0a73ec236ec3ddaaae9339b55fb5d6bff74724d38db33edb9"),
                ("keystream", "39ed6e63310f65a30083d55496aab70575823d5f39149402054c6ebf8f7f2bf1"),
                ("depth3", "dbcc65be1cd402f2f1bccbed7a2f264f3f26f6021fa206a3114d01b0b3162785"),
                ("depth4", "7b17d8d9161e3b65ba6f1f8f912bb51efb048a357e85da9a53d88bb20a2a6436"),
                ("placed", "3c57007347fe8c493c3acb252072ef3b107e3e7a26c4ea2b3c08f3532890814f"),
                ("repair", "904b00214b7320dc722fbdd3375f6308a01f959c45ede413d63f916f31d01fd4"),
                ("clump", "06a9879d5d9b1b68421068eaee049e27965cca4ce26a1650441495e008c1e532"),
                ("bob-branch", "9097ae65beb914c64aca8f8d6a494f14842de8b10148b86ed278852d4e2b4b21"),
                ("paper", "67cb263143cbc7b2f5ef160f734b302a418454768bcc4c1770385d28e1e35828"),
                ("widths", "5df871436efb665fd2cf2bad6fa01f8c566f07ed893f87cce47e42dd92bd019e"),
                ("hole", "3b86af84c05c57f3d8496287de142c29d7aedab38ca3a9ea6005d371c68e1a06"),
                ("clerical", "264ba5d22210f0601017ab53e19fb62c1e2dab802e6738dec7315336634b15ea"),
                ("intro", "83e3341f2ccebfad15d7725b9c92cf81d0aa99eb7e54bae04909ee800ea13ade"),
                ("block", "b3435b785f0e8c3ca06b75f09b4c2a35d9d71b80a2b2f4d03002f6d16d2dfba8"),
                ("digraph", "0379eb9544a3369b5d4b2c64406d4bf7f3c99ed2cb130c9dfb7e5b757db0b712"),
                ("trigram", "8bff977b3c20bd603579390f2f158daf0863129978fe0d719df1fa1ac8a67f73"),
                ("monotone", "58d552634106ca14a8b41cf50a976c97d5fb2f3ba6180261b1a26cfdeb538a12"),
                ("straight", "a076422664824074d01d386c1ddabc5e9d99569a15fc1d1211ec4e3c14ea18ae"),
                ("diagonal", "a47afb759a9a73d2653d3c9ba0e4eca786b51731964a9b24519abc17dfbbf525"),
                ("heavy", "8b2a3f27c4955bc94db2e11295ede3e10ab2302e5dba4976cbc41b92d0ee4ef3"),
                ("spread", "44ae913903f708ee19a193b75bca1a2cfd3e0b8480934d4b3bdda1532a565c0f"),
                ("residual", "5fb0d29cc076de94610993fcce371c51969fc599c09cd780ba82d612bdd6f0ca"),
                ("sharp", "af1acd51b58c869e1f597e542e94b82efecca712ade36c0f6ec03d1adf9e0e37"),
                ("rest", "1e2d3e08d977939f0ce5de560e0325dfc6ec03ff4dcd443af4c4874711a14d10"),
                ("bob-exercise", "b39e4dead829f1807cc4199098c8e2aadc5ed171c0fbcd6f5bf02b9a7f6f91f9"),
                ("triples", "aa4c65c1a86983232f8610a828f1c06d6226ae97c9fbd3cbb9cfcb1acd97ae78"),
                ("contact", "fdbe585e34d743c42c7a539e0e3a1fe486eb730be76155f5507c3b28bf3d2c62"),
                ("meeting", "59c0cdeb9a4afa378a9ba965879020c022c775947623066b4c6892d3dedca3de"),
                ("sandwich", "3ec1bfd909dc1b349c16d4321673b1336bfff63636c8a14f4c17ade681cdd451"),
                ("outside", "5b79a8f1e005b9ec24e914b60f81e9aa35d8a5d75c087cea67e74f6cf3ab8f68"),
                ("modulo", "6b037cdc15e6c2b0b0afa207ebbc6ae678a62743c9f1243b13b44e4137c1262c"),
                ("halves", "2404731c407393404c8218c0e3e96b872fb3e6bd9921fd28acd8bb5d448639b0"),
                ("repeat", "573cf748c3d829f4e83dcb813328345bb5bf6a5792a984f038130a26f5a2fc61"),
                ("held", "523c9197603544a007f3b16a26565129bde133147edb07aab41336c675cc0885"),
                ("seats", "f9a7413f4d1e1db98cf9769702a8979592055d71a00c039f7cd190a7902918c7"),
                ("extras", "f5907b5c26613bcbb99e278517f014bd0790f28a02d8fbd55844f40f400916fb"),
                ("heldsand", "db01e89ad081e11aeec1d264b177f2a7f26a7f195805dbc833bf820102bde44c"),
                ("heldwait", "dfc4f6eaacc69220c4c648575b89fe83d731951eed5615903ef2d2ea6d846288"),
                ("quartet", "bd92001356d97a06c655f024d924cfcf6f0701e5c09f3cd30d307c245aa3a713"),
                ("squares", "88a52aaeda3bdf4b247084fbfa35f7523bd93d55d50fb8d494ef4089b91ff668"),
                ("twospace", "8c6a485614c48c8f7daad4ee71a9759c1323c3ad72fdd0eea421f133725fb2cc"),
                ("echo", "78724df77f62d2de9cdc808c02adafb4646556e2c66347528239655e46b6163e"),
                ("ride", "bd3b9c5021964df4412f843d208d46fa5d6856d1962325c9ea00465ded496111"),
                ("span", "592d4abf3b2bd4de3c2515ea538b4570373887e868fc4ac5fd9535f2a7e88176"),
                ("successive", "f59575edc6dac1619cfac3e0d7ea2b19cd3a4996d79669efb16de6284cb257dc"),
                ("counts", "8dc14f9917b195f4671f5e432136525e69ecb058f4fbabe86b9dea50803da3a1"),
                ("tile", "9257bc55494ccfa4c55a8d065f45cf1f72e66c7421f55b5812e288e00d435d05"),
                ("bob-pair", "1ed12ea6572d2fb8bbfceedc07fa67840e34ea2e3e78e863370dd213721db0a5"),
                ("bob-lift", "55316d8ee090829fa17f0f45b05b143ae8c273ca8a5dd05c47282e16010b4064"),
                ("blank", "74f5614259fe7a25d72965bb1e479edc40bfa895976f692185f40b169080b8ba"),
            ],
        )
        self.assertEqual(
            report["chain_sha256"],
            "b0b14f14f4169965e21510787b9fb5b5a847ef8f81aef9be712939eca56d6a87",
        )
        self.assertEqual(report["entries"][0]["chain_sha256"], report["entries"][0]["content_sha256"])
        self.assertNotEqual(report["entries"][1]["chain_sha256"], report["entries"][1]["content_sha256"])


if __name__ == "__main__":
    unittest.main()
